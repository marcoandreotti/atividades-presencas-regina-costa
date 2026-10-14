"""Aplicação do Registro de Atividades e Presenças."""

import os
from pathlib import Path

from flask import Flask
from sqlalchemy import create_engine, event

from app.models import Base
from app.routes import main_bp


def create_app(test_config: dict | None = None) -> Flask:
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__, instance_relative_config=True)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    app.config.from_mapping(
        DEBUG=os.environ.get("FLASK_DEBUG", "").lower() in {"1", "true"},
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            "DATABASE_URL",
            f"sqlite:///{(Path(app.instance_path) / 'atividades.db').as_posix()}",
        ),
    )
    if test_config:
        app.config.update(test_config)

    engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    if engine.dialect.name == "sqlite":
        @event.listens_for(engine, "connect")
        def enable_sqlite_foreign_keys(connection, _record):
            cursor = connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    Base.metadata.create_all(engine)
    app.extensions["database_engine"] = engine
    app.register_blueprint(main_bp)
    return app


