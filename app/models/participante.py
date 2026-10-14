"""Modelo mínimo de participante para demonstrações com dados fictícios."""

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base


class Participante(Base):
    __tablename__ = "participantes"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome_exibicao: Mapped[str] = mapped_column(String(100), nullable=False)
    codigo_referencia: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    presencas: Mapped[list["Presenca"]] = relationship(back_populates="participante")
