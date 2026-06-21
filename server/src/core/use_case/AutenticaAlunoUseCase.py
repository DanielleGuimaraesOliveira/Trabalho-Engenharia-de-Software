from src.core.interfaces.IAlunoRepository import IAlunoRepository
from src.core.interfaces.ITokenService import ITokenService


class AutenticaAlunoUseCase:

    def __init__(
        self,
        repositorio_aluno: IAlunoRepository,
        token_service: ITokenService,
        hash_service,
    ):
        self.repositorio_aluno = repositorio_aluno
        self.token_service = token_service
        self.hash_service = hash_service

    def executa(self, dto):
        aluno = self.repositorio_aluno.encontra_por_email(dto.email)

        if not aluno:
            raise Exception("Email inválido")

        senha_valida = self.hash_service.verificar(aluno.senhaHash, dto.senha)

        if not senha_valida:
            raise Exception("Senha inválida")

        token = self.token_service.gerar_token(aluno.id)

        return {
            "token": token,
            "id": aluno.id,
            "nome": aluno.nome,
            "email": aluno.email,
        }
