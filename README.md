# 🌹 Tarot Agenda

Sistema de agendamento de sessões de tarot cigano.  
Feito em Python com FastAPI.

---

## 📋 Pré-requisitos

- Conta no [GitHub](https://github.com) (gratuito)
- Conta no [Render.com](https://render.com) (gratuito)
- [Git](https://git-scm.com/downloads) instalado no seu computador

---

## 🐙 Passo 1 — Subir no GitHub

### 1.1 Criar repositório

1. Acesse [github.com](https://github.com) e faça login
2. Clique no **+** no canto superior direito → **New repository**
3. Dê o nome `tarot-agenda`
4. Deixe como **Public**
5. Clique em **Create repository**

### 1.2 Enviar os arquivos pelo terminal

Abra o terminal (Prompt de Comando) **dentro da pasta** `tarot-agenda` e rode os comandos abaixo **um por um**:

```bash
git init
git add .
git commit -m "primeiro commit"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/tarot-agenda.git
git push -u origin main
```

> ⚠️ Substitua `SEU_USUARIO` pelo seu usuário do GitHub.

---

## ☁️ Passo 2 — Publicar no Render (gratuito)

1. Acesse [render.com](https://render.com) e crie conta com o Google
2. Clique em **New +** → **Web Service**
3. Conecte sua conta do GitHub e selecione o repositório `tarot-agenda`
4. Preencha as configurações:

| Campo | Valor |
|---|---|
| **Name** | tarot-agenda |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| **Plan** | Free |

5. Clique em **Create Web Service**
6. Aguarde alguns minutos — o Render vai instalar tudo e publicar o site
7. Quando aparecer **Live** no topo, seu site está no ar! 🎉

O endereço será algo como:  
`https://tarot-agenda.onrender.com`

---

## 🔐 Painel Admin

Acesse: `https://tarot-agenda.onrender.com/admin`  
Senha padrão: `cigana2024`

> Troque a senha no arquivo `main.py`, linha:
> ```python
> ADMIN_SENHA = "cigana2024"   # ← troque aqui
> ```
> Depois de trocar, repita o passo de enviar para o GitHub:
> ```bash
> git add .
> git commit -m "troca de senha"
> git push
> ```
> O Render atualiza o site automaticamente.

---

## ⚠️ Aviso importante

O plano gratuito do Render **dorme** após 15 minutos sem visitas.  
Na próxima visita, o site pode demorar **até 1 minuto** para carregar.  
Isso é normal — basta esperar e depois funciona normalmente.

---

## 📁 Estrutura do projeto

```
tarot-agenda/
├── main.py              # Servidor principal
├── database.py          # Banco de dados SQLite
├── models.py            # Modelos de referência
├── notificacoes.py      # Notificações WhatsApp
├── requirements.txt     # Dependências Python
├── static/              # Arquivos estáticos (CSS, JS)
└── templates/
    ├── index.html       # Página pública de agendamento
    ├── admin.html       # Painel da tarologa
    └── admin_login.html # Login do painel
```

---

Feito com 🌹 para tarot cigano.
