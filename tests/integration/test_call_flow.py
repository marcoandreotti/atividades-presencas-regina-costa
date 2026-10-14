"""Verifica persistência e resposta das rotas da chamada."""

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Atividade, Participante, Presenca


def criar_dados_ficticios(app):
    engine = app.extensions["database_engine"]
    with Session(engine) as session:
        atividade = Atividade(titulo="Roda demonstrativa", data=date(2026, 12, 12))
        pessoas = [
            Participante(nome_exibicao=f"Participante {numero:02d}", codigo_referencia=f"TST-{numero:03d}")
            for numero in range(1, 4)
        ]
        session.add_all([atividade, *pessoas])
        session.commit()
        return atividade.id, [pessoa.id for pessoa in pessoas]


def test_chamada_salva_presencas_e_apresenta_resultado_persistido(app, client):
    activity_id, participant_ids = criar_dados_ficticios(app)

    response = client.get(f"/atividades/{activity_id}/chamada")
    assert response.status_code == 200
    assert b"Participante 01" in response.data
    assert b"aria-pressed=\"false\"" in response.data

    response = client.post(
        f"/atividades/{activity_id}/chamada",
        data={
            f"participante-{participant_ids[0]}": "presente",
            f"participante-{participant_ids[1]}": "ausente",
            f"participante-{participant_ids[2]}": "presente",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Chamada registrada" in response.data
    assert b"Participantes registrados</dt><dd>3" in response.data
    assert b"Presentes</dt><dd>2" in response.data
    assert b"Ausentes</dt><dd>1" in response.data

    with Session(app.extensions["database_engine"]) as session:
        registros = session.scalars(
            select(Presenca).where(Presenca.atividade_id == activity_id)
        ).all()
        assert len(registros) == 3
        assert session.get(Atividade, activity_id).status == "realizada"


def test_chamada_rejeita_envio_incompleto_com_orientacao_textual(app, client):
    activity_id, participant_ids = criar_dados_ficticios(app)

    response = client.post(
        f"/atividades/{activity_id}/chamada",
        data={f"participante-{participant_ids[0]}": "presente"},
    )

    assert response.status_code == 400
    assert b"Marque Presente ou Ausente para cada participante" in response.data
    with Session(app.extensions["database_engine"]) as session:
        assert session.scalars(select(Presenca)).all() == []
