"""Fixtures compartilhadas pelos testes automatizados."""

import pytest

from app import create_app


@pytest.fixture
def app(tmp_path):
    """Cria a aplicação ligada a um banco SQLite temporário."""
    database_path = tmp_path / "testes.db"
    application = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path.as_posix()}",
        }
    )

    yield application

    application.extensions["database_engine"].dispose()


@pytest.fixture
def client(app):
    """Disponibiliza o cliente HTTP de teste do Flask."""
    return app.test_client()
