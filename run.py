"""Ponto de entrada para executar a aplicação Flask localmente."""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
