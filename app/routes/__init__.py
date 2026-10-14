"""Rotas HTTP do fluxo de atividades e chamadas."""

from sqlalchemy import select
from flask import Blueprint, abort, current_app, redirect, render_template, request, url_for
from sqlalchemy.orm import Session

from app.models import Atividade, Participante, Presenca

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def index():
    """Lista as atividades demonstrativas disponíveis para a equipe."""
    engine = _engine()
    with Session(engine) as session:
        atividades = session.scalars(
            select(Atividade).order_by(Atividade.data, Atividade.horario, Atividade.titulo)
        ).all()
        return render_template("index.html", atividades=atividades)


@main_bp.route("/atividades/<int:activity_id>/chamada", methods=["GET", "POST"])
def chamada(activity_id: int):
    """Exibe e salva uma chamada com uma situação por participante ativo."""
    engine = _engine()
    with Session(engine) as session:
        atividade = session.get(Atividade, activity_id)
        if atividade is None:
            abort(404)

        participantes = session.scalars(
            select(Participante)
            .where(Participante.ativo.is_(True))
            .order_by(Participante.nome_exibicao)
        ).all()
        registros = session.scalars(
            select(Presenca).where(Presenca.atividade_id == activity_id)
        ).all()
        situacoes = {registro.participante_id: registro.situacao for registro in registros}

        if request.method == "POST":
            selecoes = {
                participante.id: request.form.get(f"participante-{participante.id}", "")
                for participante in participantes
            }
            if not participantes or any(valor not in {"presente", "ausente"} for valor in selecoes.values()):
                return render_template(
                    "chamada.html",
                    atividade=atividade,
                    participantes=participantes,
                    situacoes=selecoes,
                    erro="Marque Presente ou Ausente para cada participante antes de salvar.",
                ), 400

            por_participante = {registro.participante_id: registro for registro in registros}
            for participante_id, situacao in selecoes.items():
                registro = por_participante.get(participante_id)
                if registro is None:
                    registro = Presenca(
                        atividade_id=activity_id,
                        participante_id=participante_id,
                        situacao=situacao,
                    )
                    session.add(registro)
                else:
                    registro.situacao = situacao
            atividade.status = "realizada"
            session.commit()
            return redirect(url_for("main.resultado", activity_id=activity_id))

        return render_template(
            "chamada.html",
            atividade=atividade,
            participantes=participantes,
            situacoes=situacoes,
            erro=None,
        )


@main_bp.get("/atividades/<int:activity_id>/resultado")
def resultado(activity_id: int):
    """Apresenta os totais da chamada salvos no banco local."""
    engine = _engine()
    with Session(engine) as session:
        atividade = session.get(Atividade, activity_id)
        if atividade is None:
            abort(404)
        registros = session.scalars(
            select(Presenca).where(Presenca.atividade_id == activity_id)
        ).all()
        linhas = [
            {"nome": registro.participante.nome_exibicao, "situacao": registro.situacao}
            for registro in registros
        ]
        presentes = sum(linha["situacao"] == "presente" for linha in linhas)
        ausentes = len(linhas) - presentes
        return render_template(
            "resultado.html",
            atividade=atividade,
            linhas=linhas,
            presentes=presentes,
            ausentes=ausentes,
        )


def _engine():
    return current_app.extensions["database_engine"]
