"""Modelo de atividade do Núcleo."""

from datetime import date, time

from sqlalchemy import CheckConstraint, Date, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base


class Atividade(Base):
    __tablename__ = "atividades"
    __table_args__ = (
        CheckConstraint("status IN ('planejada', 'realizada', 'cancelada')", name="ck_atividade_status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(120), nullable=False)
    data: Mapped[date] = mapped_column(Date, nullable=False)
    horario: Mapped[time | None] = mapped_column(Time, nullable=True)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(12), nullable=False, default="planejada")

    presencas: Mapped[list["Presenca"]] = relationship(back_populates="atividade")
