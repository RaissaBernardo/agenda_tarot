import sqlite3
from contextlib import contextmanager

DB_PATH = "agenda.db"


def init_db():
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS agendamentos (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                nome       TEXT NOT NULL,
                whatsapp   TEXT,
                servico    TEXT NOT NULL,
                preco      TEXT,
                data       TEXT NOT NULL,
                horario    TEXT NOT NULL,
                pagamento  TEXT,
                status     TEXT DEFAULT 'pendente',
                criado_em  TEXT
            );

            CREATE TABLE IF NOT EXISTS servicos (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                nome    TEXT NOT NULL,
                preco   TEXT NOT NULL,
                duracao TEXT NOT NULL,
                icone   TEXT DEFAULT '🃏',
                ativo   INTEGER DEFAULT 1
            );
        """)
        existe = conn.execute("SELECT COUNT(*) FROM servicos").fetchone()[0]
        if not existe:
            conn.executemany(
                "INSERT INTO servicos (nome, preco, duracao, icone) VALUES (?,?,?,?)",
                [
                    ("Perguntas individuais",       "R$ 20",  "10–15 min por pergunta", "🃏"),
                    ("Tarot completo — vídeo",       "R$ 80",  "60 min",                 "📹"),
                    ("Tarot completo — WhatsApp",    "R$ 70",  "70 min",                 "💬"),
                    ("Mesa do amor",                 "R$ 60",  "30 min",                 "🌹"),
                    ("Tarot premium anual",          "R$ 700", "60 min/mês · 12 sessões","✨"),
                ]
            )
        conn.commit()


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
