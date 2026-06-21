from flask import request
from flask_openapi3 import Tag

from src.app.schemas import ( AlunoSchema, LoginSchema, ErrorSchema, AlunoViewSchema)
from src.core.dto.AlunoDTO import AlunoDTO
from src.core.dto.LoginDTO import LoginDTO
from src.core.use_case.CriaAlunoUseCase import CriaAlunoUseCase
from src.core.use_case.AutenticaAlunoUseCase import AutenticaAlunoUseCase


aluno_tag = Tag(name="Aluno", description="Cadastro e autenticação de alunos")


def register_aluno_routes(app, cria_aluno_use_case: CriaAlunoUseCase, auth_use_case: AutenticaAlunoUseCase, token_service=None, repositorio_aluno=None):
    @app.post("/aluno", tags=[aluno_tag], responses={"200": AlunoViewSchema, "400": ErrorSchema })
    def cria_aluno(body: AlunoSchema):
        try:
            dto = AlunoDTO(nome=body.nome, email=body.email, senha=body.senha)
            cria_aluno_use_case.executa(dto)

            return {"message": "Aluno criado com sucesso" }, 200

        except Exception as error:
            return {"message": str(error)}, 400

    @app.post("/login", tags=[aluno_tag], responses={"200": AlunoViewSchema, "401": ErrorSchema})
    def login(body: LoginSchema):
        try:
            dto = LoginDTO( email=body.email, senha=body.senha)
            resultado = auth_use_case.executa(dto)

            return resultado, 200

        except Exception as error:
            return {"message": str(error)}, 401

    @app.get("/aluno/me", tags=[aluno_tag], responses={"200": AlunoViewSchema, "401": ErrorSchema})
    def aluno_logado():
        try:
            auth_header = request.headers.get("Authorization", "")

            if not auth_header.startswith("Bearer "):
                raise Exception("Token não informado")

            token = auth_header.replace("Bearer ", "", 1)

            aluno_id = token_service.decodifica_token(token)

            aluno = repositorio_aluno.encontra_por_id(aluno_id)

            if not aluno:
                raise Exception("Aluno não encontrado")

            return {"id": aluno.id, "nome": aluno.nome, "email": aluno.email}, 200

        except Exception as error:
            return {"message": str(error)}, 401