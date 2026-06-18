from typing import List
from pydantic import BaseModel
from src.core.entities.Materia import Materia

class MateriaSchema(BaseModel):
    id: int
    nome: str
    codigo: str
    departamento: str


class ListagemMateriasSchema(BaseModel):
    materias: List[MateriaSchema]


def apresenta_materia(materia: Materia):
    return {
        "id": materia.id,
        "nome": materia.nome,
        "codigo": materia.codigo,
        "departamento": materia.departamento.name
    }


def apresenta_materias(materias: list[Materia]):
    return {
        "materias": [
            {
                "id": materia.id,
                "nome": materia.nome,
                "codigo": materia.codigo,
                "departamento": materia.departamento.name
            }
            for materia in materias
        ]
    }