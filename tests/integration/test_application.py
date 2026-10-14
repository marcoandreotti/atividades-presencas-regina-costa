"""Testes de integração das rotas e da inicialização da aplicação."""

from sqlalchemy import inspect


def test_pagina_inicial_exibe_orientacao_de_demonstracao(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b'<html lang="pt-BR">' in response.data
    assert b"Registro de Atividades" in response.data
    assert b"somente dados" in response.data


def test_aplicacao_cria_tabelas_no_banco_configurado(app):
    engine = app.extensions["database_engine"]

    assert set(inspect(engine).get_table_names()) == {
        "atividades",
        "participantes",
        "presencas",
    }
