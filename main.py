from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from datetime import datetime, date
import uvicorn

from database import init_db, get_db
from notificacoes import enviar_whatsapp

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Tarot Agenda", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ─── ROTAS PÚBLICAS ──────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/horarios-disponiveis")
def horarios_disponiveis(data: str):
    try:
        d = date.fromisoformat(data)
    except ValueError:
        raise HTTPException(status_code=400, detail="Data inválida")

    dia_semana = d.weekday()  # 0=seg … 6=dom
    fim_de_semana = dia_semana >= 5

    todos = ["09:00","10:00","11:00","14:00","15:00","16:00","17:00","18:00"] if fim_de_semana else ["17:00"]

    with get_db() as conn:
        ocupados = conn.execute(
            "SELECT horario FROM agendamentos WHERE data=? AND status!='cancelado'", (data,)
        ).fetchall()
        ocupados_set = {row[0] for row in ocupados}

    return {"data": data, "horarios": [h for h in todos if h not in ocupados_set]}


@app.post("/api/agendar")
async def agendar(request: Request):
    body = await request.json()
    nome     = body.get("nome","").strip()
    whatsapp = body.get("whatsapp","").strip()
    servico  = body.get("servico","").strip()
    preco    = body.get("preco","").strip()
    data     = body.get("data","").strip()
    horario  = body.get("horario","").strip()
    pagamento= body.get("pagamento","").strip()

    if not all([nome, servico, data, horario]):
        raise HTTPException(status_code=422, detail="Campos obrigatórios faltando")

    with get_db() as conn:
        existe = conn.execute(
            "SELECT id FROM agendamentos WHERE data=? AND horario=? AND status!='cancelado'",
            (data, horario)
        ).fetchone()
        if existe:
            raise HTTPException(status_code=409, detail="Horário já ocupado")

        conn.execute(
            """INSERT INTO agendamentos
               (nome, whatsapp, servico, preco, data, horario, pagamento, status, criado_em)
               VALUES (?,?,?,?,?,?,?,'pendente',?)""",
            (nome, whatsapp, servico, preco, data, horario, pagamento, datetime.now().isoformat())
        )
        conn.commit()

    try:
        if whatsapp:
            enviar_whatsapp(nome, whatsapp, servico, data, horario)
    except Exception:
        pass

    return {"ok": True, "mensagem": "Agendamento realizado com sucesso!"}


# ─── ADMIN ───────────────────────────────────────────────────────────────────

ADMIN_SENHA = "cigana2024"  # ← troque para uma senha forte


@app.get("/admin", response_class=HTMLResponse)
def admin_login(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})


@app.post("/admin/login")
def admin_login_post(request: Request, senha: str = Form(...)):
    if senha != ADMIN_SENHA:
        return templates.TemplateResponse("admin_login.html", {"request": request, "erro": "Senha incorreta"})
    response = RedirectResponse("/admin/painel", status_code=302)
    response.set_cookie("admin_auth", ADMIN_SENHA, httponly=True)
    return response


def check_admin(request: Request):
    if request.cookies.get("admin_auth") != ADMIN_SENHA:
        raise HTTPException(status_code=401, detail="Não autorizado")


@app.get("/admin/painel", response_class=HTMLResponse)
def admin_painel(request: Request):
    check_admin(request)
    with get_db() as conn:
        agendamentos = conn.execute(
            "SELECT * FROM agendamentos ORDER BY data DESC, horario DESC"
        ).fetchall()
    return templates.TemplateResponse("admin.html", {"request": request, "agendamentos": agendamentos})


@app.post("/admin/agendamento/{id}/status")
def atualizar_status(id: int, request: Request, status: str = Form(...)):
    check_admin(request)
    with get_db() as conn:
        conn.execute("UPDATE agendamentos SET status=? WHERE id=?", (status, id))
        conn.commit()
    return RedirectResponse("/admin/painel", status_code=302)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
