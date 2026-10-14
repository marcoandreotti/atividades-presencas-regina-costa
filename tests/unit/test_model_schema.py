"""Testes unitários das restrições declaradas no esquema do domínio."""

from app.models import Atividade, Participante, Presenca


def test_atividade_exige_titulo_e_data_e_restringe_status():
    assert Atividade.__table__.c.titulo.nullable is False
    assert Atividade.__table__.c.data.nullable is False

    status_check = next(
        constraint
        for constraint in Atividade.__table__.constraints
        if constraint.name == "ck_atividade_status"
    )
    assert "planejada" in str(status_check.sqltext)
    assert "realizada" in str(status_check.sqltext)
    assert "cancelada" in str(status_check.sqltext)


def test_participante_exige_codigo_de_referencia_unico():
    codigo = Participante.__table__.c.codigo_referencia

    assert codigo.nullable is False
    assert codigo.unique is True


def test_presenca_impede_repeticao_e_restringe_situacao():
    constraints = Presenca.__table__.constraints
    presenca_unica = next(
        constraint
        for constraint in constraints
        if constraint.name == "uq_presenca_atividade_participante"
    )
    situacao_check = next(
        constraint
        for constraint in constraints
        if constraint.name == "ck_presenca_situacao"
    )

    assert {column.name for column in presenca_unica.columns} == {
        "atividade_id",
        "participante_id",
    }
    assert "presente" in str(situacao_check.sqltext)
    assert "ausente" in str(situacao_check.sqltext)
