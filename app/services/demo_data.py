"""Criação idempotente de dados fictícios para execução local."""

from datetime import date, time

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Atividade, Participante


def ensure_demo_data(engine) -> None:
    """Popula a base vazia do ambiente local com conteúdo explicitamente fictício."""
    with Session(engine) as session:
        if session.scalar(select(func.count()).select_from(Atividade)):
            return

        atividade = Atividade(
            titulo="Roda de conversa",
            data=date(2026, 12, 12),
            horario=time(10, 0),
            descricao="Encontro demonstrativo para troca de experiências.",
        )
        participantes = [
            Participante(nome_exibicao=f"Participante {numero:02d}", codigo_referencia=f"DEMO-{numero:03d}")
            for numero in range(1, 4)
        ]
        session.add_all([atividade, *participantes])
        session.commit()
