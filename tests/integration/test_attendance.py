"""Testes de integração das relações e restrições de presença no SQLite."""

from datetime import date

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Atividade, Participante, Presenca


def test_registra_presenca_e_carrega_relacionamentos(app):
    engine = app.extensions["database_engine"]

    with Session(engine) as session:
        atividade = Atividade(titulo="Oficina de convivência", data=date(2026, 10, 14))
        participante = Participante(
            nome_exibicao="Pessoa de demonstração",
            codigo_referencia="DEMO-001",
        )
        presenca = Presenca(
            atividade=atividade,
            participante=participante,
            situacao="presente",
        )
        session.add(presenca)
        session.commit()

        assert presenca.id is not None
        assert presenca.atividade.titulo == "Oficina de convivência"
        assert presenca.participante.codigo_referencia == "DEMO-001"
        assert participante.ativo is True


def test_banco_rejeita_presenca_duplicada_para_mesma_atividade_e_pessoa(app):
    engine = app.extensions["database_engine"]

    with Session(engine) as session:
        atividade = Atividade(titulo="Roda de conversa", data=date(2026, 10, 14))
        participante = Participante(
            nome_exibicao="Pessoa de demonstração",
            codigo_referencia="DEMO-002",
        )
        session.add_all([atividade, participante])
        session.flush()
        session.add_all(
            [
                Presenca(atividade=atividade, participante=participante, situacao="presente"),
                Presenca(atividade=atividade, participante=participante, situacao="ausente"),
            ]
        )

        with pytest.raises(IntegrityError):
            session.commit()


def test_banco_rejeita_situacao_de_presenca_fora_dos_valores_permitidos(app):
    engine = app.extensions["database_engine"]

    with Session(engine) as session:
        atividade = Atividade(titulo="Atividade de teste", data=date(2026, 10, 14))
        participante = Participante(
            nome_exibicao="Pessoa de demonstração",
            codigo_referencia="DEMO-003",
        )
        session.add_all([atividade, participante])
        session.flush()
        session.add(
            Presenca(atividade=atividade, participante=participante, situacao="talvez")
        )

        with pytest.raises(IntegrityError):
            session.commit()
