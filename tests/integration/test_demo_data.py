"""Verifica a semeadura repetível de registros apenas demonstrativos."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Atividade, Participante
from app.services.demo_data import ensure_demo_data


def test_base_vazia_recebe_atividade_e_pessoas_ficticias_sem_duplicar(app):
    engine = app.extensions["database_engine"]

    ensure_demo_data(engine)
    ensure_demo_data(engine)

    with Session(engine) as session:
        atividades = session.scalars(select(Atividade)).all()
        participantes = session.scalars(select(Participante)).all()

    assert len(atividades) == 1
    assert atividades[0].titulo == "Roda de conversa"
    assert len(participantes) == 3
    assert {p.codigo_referencia for p in participantes} == {"DEMO-001", "DEMO-002", "DEMO-003"}
