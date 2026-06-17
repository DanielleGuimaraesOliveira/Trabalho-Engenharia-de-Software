from src.core.entities.Aluno import Aluno
from src.infra.db.model.aluno_model import AlunoModel


class AlunoMapper:

    @staticmethod
    def to_model(aluno: Aluno) -> AlunoModel:

        return AlunoModel(nome=aluno.nome, email=aluno.email, senha=aluno.senhaHash)
    
    @staticmethod
    def to_entity(model: AlunoModel) -> Aluno:
        return Aluno(id=model.id, nome=model.nome, email=model.email, senhaHash=model.senha)