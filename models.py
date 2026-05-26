# Modelos de dados (referência – banco usa SQLite direto)

class Agendamento:
    id: int
    nome: str
    email: str
    whatsapp: str
    servico: str
    preco: str
    data: str
    horario: str
    pagamento: str
    status: str  # pendente | confirmado | cancelado
    criado_em: str


class Servico:
    id: int
    nome: str
    preco: str
    duracao: str
    icone: str
    ativo: bool


class ConfigHorario:
    """
    Semana  → apenas 17:00
    Fim de semana → 09:00 10:00 11:00 14:00 15:00 16:00 17:00 18:00
    """
    pass
