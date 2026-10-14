"""Modelos relacionais do domínio do MVP."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base comum dos modelos SQLAlchemy."""


from app.models.atividade import Atividade
from app.models.participante import Participante
from app.models.presenca import Presenca

__all__ = ["Atividade", "Base", "Participante", "Presenca"]
