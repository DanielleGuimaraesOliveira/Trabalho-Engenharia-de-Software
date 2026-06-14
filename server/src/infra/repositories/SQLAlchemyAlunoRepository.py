from core.entities.Aluno import Aluno
from core.interfaces.IAlunoRepository import IAlunoRepository

class SQLAlchemyAlunoRepositorio(IAlunoRepository):
    def __init__(self, session):
        self.session = session

    def salva(self, aluno: Aluno) -> bool:
        self.session.add(aluno)
        self.session.commit()
        return True

    def encontra_por_id(self, id: int) -> Aluno:
        return (self.session.query(Aluno).filter_by(id=id).first())

    def encontra_por_email(self, email: str) -> Aluno:
        return (
            self.session.query(Aluno).filter_by(email=email).first()
        )