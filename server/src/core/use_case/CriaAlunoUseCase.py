from src.core.entities.Aluno import Aluno
from src.core.interfaces.IAlunoRepository import IAlunoRepository


class CriaAlunoUseCase:
    def __init__(self, repositorio_aluno: IAlunoRepository, senha_hash):
        self.repositorio_aluno = repositorio_aluno
        self.senha_hash = senha_hash

    def executa(self, dto):

        senha_criptografada = self.senha_hash.hash(dto.senha)

        aluno = Aluno(nome=dto.nome, email=dto.email,senhaHash=senha_criptografada)

        self.repositorio_aluno.salva(aluno)

        return dto