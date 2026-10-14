"""Modelo de presença associado a uma atividade e participante."""

from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base


class Presenca(Base):
    __tablename__ = "presencas"
    __table_args__ = (
        UniqueConstraint("atividade_id", "participante_id", name="uq_presenca_atividade_participante"),
        CheckConstraint("situacao IN ('presente', 'ausente')", name="ck_presenca_situacao"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    atividade_id: Mapped[int] = mapped_column(ForeignKey("atividades.id", ondelete="RESTRICT"), nullable=False)
    participante_id: Mapped[int] = mapped_column(ForeignKey("participantes.id", ondelete="RESTRICT"), nullable=False)
    situacao: Mapped[str] = mapped_column(nullable=False)
    registrado_em: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)

    atividade: Mapped["Atividade"] = relationship(back_populates="presencas")
    participante: Mapped["Participante"] = relationship(back_populates="presencas")
