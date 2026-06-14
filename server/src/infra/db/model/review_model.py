from typing import Optional
from sqlalchemy import (Column, ForeignKey, Integer, String)
from sqlalchemy.orm import relationship
from src.infra.db.base import Base


class ReviewModel(Base):

    __tablename__ = "review"

    id: Optional[int] = Column("pk_review", Integer, primary_key=True)
    comentario = Column(String(255), nullable = False)
    nota = Column(Integer, nullable=False)
    id_aluno = Column(Integer, ForeignKey("aluno.pk_aluno"), nullable=False)
    id_materia = Column(Integer, ForeignKey("materia.pk_materia"), nullable=False)

    aluno = relationship("AlunoModel", back_populates="reviews")
    materia = relationship("MateriaModel", back_populates="reviews")