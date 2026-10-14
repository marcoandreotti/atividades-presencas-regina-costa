"""Consulta agregada de chamadas dentro de um mês civil."""

from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.models import Atividade, Presenca


def summarize_month(session: Session, inicio, fim):
    """Retorna totais mensais e subtotais por atividade, sem expor nomes."""
    presentes = func.coalesce(
        func.sum(case((Presenca.situacao == "presente", 1), else_=0)), 0
    )
    ausentes = func.coalesce(
        func.sum(case((Presenca.situacao == "ausente", 1), else_=0)), 0
    )
    resultados = session.execute(
        select(
            Atividade.id,
            Atividade.titulo,
            Atividade.data,
            func.count(Presenca.id).label("participantes_registrados"),
            presentes.label("presentes"),
            ausentes.label("ausentes"),
        )
        .outerjoin(Presenca, Presenca.atividade_id == Atividade.id)
        .where(Atividade.data >= inicio, Atividade.data < fim)
        .group_by(Atividade.id, Atividade.titulo, Atividade.data)
        .order_by(Atividade.data, Atividade.titulo)
    ).all()
    totais = {
        "atividades": len(resultados),
        "participantes_registrados": sum(row.participantes_registrados for row in resultados),
        "presentes": sum(row.presentes for row in resultados),
        "ausentes": sum(row.ausentes for row in resultados),
    }
    return resultados, totais
