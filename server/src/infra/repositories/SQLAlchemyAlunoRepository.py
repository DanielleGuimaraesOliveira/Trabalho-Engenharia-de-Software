from src.core.entities.Aluno import Aluno
from src.core.interfaces.IAlunoRepository import IAlunoRepository
from src.infra.db.model.aluno_model import AlunoModel
from src.infra.mappers.AlunoMapper import AlunoMapper


class SQLAlchemyAlunoRepositorio(IAlunoRepository):
    def __init__(self, session):
        self.session = session

    def salva(self, aluno: Aluno) -> bool:
        model = AlunoMapper.to_model(aluno)

        self.session.add(model)
        self.session.commit()

        return True

    def encontra_por_id(self, id: int) -> Aluno:
        model = self.session.query(AlunoModel).filter_by(id=id).first()

        if not model:
            return None

        return AlunoMapper.to_entity(model)

    def encontra_por_email(self, email: str) -> Aluno:
        model = self.session.query(AlunoModel).filter_by(email=email).first()

        if not model:
            return None

        return AlunoMapper.to_entity(model)
