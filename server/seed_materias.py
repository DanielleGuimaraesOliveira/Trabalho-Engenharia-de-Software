# seed_materias.py
from src.infra.db.model.review_model import ReviewModel
from src.infra.db.model.aluno_model import AlunoModel
from src.core.entities.Materia import Materia
from src.core.enums.departamento import Departamento
from src.infra.db.session import SessionLocal
from src.infra.repositories.SQLAlchemyMateriaRepository import (
    SQLAlchemyMateriaRepositorio
)

session = SessionLocal()
repo = SQLAlchemyMateriaRepositorio(session)

materias = [
    Materia(
        id=None,
        nome="Cálculo a Várias Variáveis I",
        codigo="MAT4162",
        departamento=Departamento.MATEMATICA
    ),
    Materia(
        id=None,
        nome="Estruturas de Dados Avançadas",
        codigo="INF1010",
        departamento=Departamento.INFORMATICA
    ),
    Materia(
        id=None,
        nome="Projeto Integrado - Sustentabilidade",
        codigo="ENG4010",
        departamento=Departamento.ENGENHARIA
    )
]

for materia in materias:
    try:
        repo.salva(materia)
        print(f"Matéria {materia.nome} criada")
    except Exception as e:
        print(f"Erro ao criar {materia.nome}: {e}")

session.close()