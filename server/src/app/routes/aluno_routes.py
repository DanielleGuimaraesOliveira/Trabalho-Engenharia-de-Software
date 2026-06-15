from flask_openapi3 import Tag

from src.app.schemas import ( AlunoSchema, LoginSchema, ErrorSchema, AlunoViewSchema)
from src.core.dto.AlunoDTO import AlunoDTO
from src.core.dto.LoginDTO import LoginDTO
from src.core.use_case.CriaAlunoUseCase import CriaAlunoUseCase
from src.core.use_case.AutenticaAlunoUseCase import AutenticaAlunoUseCase


aluno_tag = Tag(name="Aluno", description="Cadastro e autenticação de alunos")


def register_aluno_routes(app,cria_aluno_use_case: CriaAlunoUseCase, auth_use_case: AutenticaAlunoUseCase):
    @app.post("/aluno", tags=[aluno_tag], responses={"200": AlunoViewSchema, "400": ErrorSchema })
    def cria_aluno(body: AlunoSchema):
        try:
            dto = AlunoDTO(nome=body.nome, email=body.email, senha=body.senha)
            cria_aluno_use_case.executa(dto)

            return {"message": "Aluno criado com sucesso" }, 200

        except Exception as error:
            return {"message": str(error)}, 400

    @app.post("/login", tags=[aluno_tag], responses={"200": AlunoViewSchema, "401": ErrorSchema})
    def login(form: LoginSchema):
        try:
            dto = LoginDTO( email=form.email, senha=form.senha)
            resultado = auth_use_case.executa(dto)

            return resultado, 200

        except Exception as error:
            return {"message": str(error)}, 401