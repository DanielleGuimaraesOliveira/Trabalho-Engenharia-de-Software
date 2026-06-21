from flask_openapi3 import OpenAPI, Info
from flask_cors import CORS
from src.infra.db.base import Base
from src.infra.db.session import engine, SessionLocal

# MODELS
from src.infra.db.model.aluno_model import AlunoModel
from src.infra.db.model.review_model import ReviewModel
from src.infra.db.model.materia_model import MateriaModel

# REPOSITORIES
from src.infra.repositories.SQLAlchemyAlunoRepository import SQLAlchemyAlunoRepositorio
from src.infra.repositories.SQLAlchemyReviewRepository import (
    SQLAlchemyReviewRepositorio,
)
from src.infra.repositories.SQLAlchemyMateriaRepository import (
    SQLAlchemyMateriaRepositorio,
)

# SECURITY
from src.infra.security.HashService import HashService
from src.infra.security.JWTTokenService import JWTTokenService

# USE CASES
from src.core.use_case.CriaAlunoUseCase import CriaAlunoUseCase
from src.core.use_case.ListaMateriasUseCase import ListaMateriasUseCase
from src.core.use_case.ListaMateriaPorIdUseCase import ListaMateriaPorIdUseCase
from src.core.use_case.AutenticaAlunoUseCase import AutenticaAlunoUseCase
from src.core.use_case.PublicaReviewUseCase import PublicarReviewUseCase
from src.core.use_case.ListaTodasAsReviewsUseCase import ListaReviewsUseCase

# ROUTES
from src.app.routes.aluno_routes import register_aluno_routes
from src.app.routes.review_routes import register_review_routes
from src.app.routes.materia_routes import register_materia_routes

info = Info(title="API Reviews", version="1.0.0")

app = OpenAPI(__name__, info=info)

CORS(app)


@app.get("/")
def home():
    return {"message": "API funcionando"}, 200


# =========================================
# BANCO
# =========================================

Base.metadata.create_all(bind=engine)
session = SessionLocal()

# =========================================
# REPOSITORIES
# =========================================

aluno_repository = SQLAlchemyAlunoRepositorio(session)
review_repository = SQLAlchemyReviewRepositorio(session)
materia_repository = SQLAlchemyMateriaRepositorio(session)

# =========================================
# SERVICES
# =========================================

hash_service = HashService()
token_service = JWTTokenService()

# =========================================
# USE CASES
# =========================================

cria_aluno_use_case = CriaAlunoUseCase(
    repositorio_aluno=aluno_repository, senha_hash=hash_service
)

auth_aluno_use_case = AutenticaAlunoUseCase(
    repositorio_aluno=aluno_repository,
    token_service=token_service,
    hash_service=hash_service,
)

publica_review_use_case = PublicarReviewUseCase(
    repositorio_aluno=aluno_repository,
    repositorio_materia=materia_repository,
    repositorio_review=review_repository,
)

lista_reviews_use_case = ListaReviewsUseCase(
    repositorio_review=review_repository,
    repositorio_materia=materia_repository,
    repositorio_aluno=aluno_repository,
)

lista_materias_use_case = ListaMateriasUseCase(
    repositorio_materia=materia_repository)

lista_materia_por_id_use_case = ListaMateriaPorIdUseCase(
    repositorio_materia=materia_repository
)

# =========================================
# ROUTES
# =========================================

register_aluno_routes(
    app, cria_aluno_use_case, auth_aluno_use_case, aluno_repository, token_service
)
register_review_routes(app, publica_review_use_case, lista_reviews_use_case)
register_materia_routes(app, lista_materias_use_case,
                        lista_materia_por_id_use_case)

# =========================================
# RUN
# =========================================

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)
