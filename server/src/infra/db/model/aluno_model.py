from typing import Optional
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.infra.db.base import Base


class AlunoModel(Base):
    __tablename__ = "aluno"

    id: Optional[int] = Column("pk_aluno", Integer, primary_key=True)
    nome = Column(String(140), nullable=False)
    email = Column(String(140), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)

    reviews = relationship(
        "ReviewModel",
        back_populates="aluno",
        cascade="all, delete-orphan",
        lazy="joined",
    )
