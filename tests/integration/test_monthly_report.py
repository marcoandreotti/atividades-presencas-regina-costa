"""Verifica filtro por mês e agregação sem dados pessoais no relatório."""

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Atividade, Participante, Presenca


def test_relatorio_agrega_chamadas_do_mes_selecionado(app, client):
    engine = app.extensions["database_engine"]
    with Session(engine) as session:
        dezembro = Atividade(titulo="Roda de conversa", data=date(2026, 12, 12))
        dezembro_2 = Atividade(titulo="Oficina", data=date(2026, 12, 20))
        janeiro = Atividade(titulo="Encontro posterior", data=date(2027, 1, 3))
        pessoas = [
            Participante(nome_exibicao=f"Pessoa teste {n}", codigo_referencia=f"RPT-{n}")
            for n in range(1, 4)
        ]
        session.add_all([dezembro, dezembro_2, janeiro, *pessoas])
        session.flush()
        session.add_all(
            [
                Presenca(atividade_id=dezembro.id, participante_id=pessoas[0].id, situacao="presente"),
                Presenca(atividade_id=dezembro.id, participante_id=pessoas[1].id, situacao="ausente"),
                Presenca(atividade_id=dezembro_2.id, participante_id=pessoas[2].id, situacao="presente"),
            ]
        )
        session.commit()

    response = client.get("/relatorios?mes=2026-12")

    assert response.status_code == 200
    assert b"Totais do per\xc3\xadodo" in response.data
    assert b"Roda de conversa" in response.data
    assert b"Oficina" in response.data
    assert b"Encontro posterior" not in response.data
    assert b"Pessoa teste" not in response.data
    assert b"<dt>Atividades</dt><dd>2</dd>" in response.data
    assert b"<dt>Presen\xc3\xa7as</dt><dd>2</dd>" in response.data
    assert b"<dt>Aus\xc3\xaancias</dt><dd>1</dd>" in response.data


def test_relatorio_sem_atividades_no_mes_informa_estado_vazio(client):
    response = client.get("/relatorios?mes=2026-11")

    assert response.status_code == 200
    assert b"Nenhuma atividade neste m\xc3\xaas" in response.data


def test_relatorio_corrige_mes_invalido_para_mes_da_atividade_mais_recente(app, client):
    with Session(app.extensions["database_engine"]) as session:
        session.add(Atividade(titulo="Teste", data=date(2026, 12, 12)))
        session.commit()

    response = client.get("/relatorios?mes=nao-e-mes")

    assert response.status_code == 200
    assert b'value="2026-12"' in response.data
    assert b"Teste" in response.data
