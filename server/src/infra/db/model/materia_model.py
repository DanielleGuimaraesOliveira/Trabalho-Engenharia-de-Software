from typing import Optional
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.infra.db.base import Base


class MateriaModel(Base):

    __tablename__ = "materia"

    id: Optional[int] = Column("pk_materia", Integer, primary_key=True)
    nome = Column(String(140), unique=True, nullable=False)
    descricao = Column( String(255), nullable=True)

    reviews = relationship("ReviewModel", back_populates="materia", cascade="all, delete-orphan", lazy="joined")