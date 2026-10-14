"""Rotas HTTP da aplicação."""

from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def index():
    """Apresenta a página inicial enquanto os fluxos do MVP são implementados."""
    return render_template("index.html")
