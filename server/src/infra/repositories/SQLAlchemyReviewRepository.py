from core.entities.Review import Review
from core.interfaces.IReviewRepository import IReviewRepository


class SQLAlchemyReviewRepositorio(IReviewRepository):
    def __init__(self, session):
        self.session = session

    def salva(self, review: Review) -> None:
        self.session.add(review)
        self.session.commit()

    def encontra_por_materia(self, id_materia: int) -> list[Review]:
        return (self.session.query(Review).filter_by(id_materia=id_materia).all())

    def encontra_por_usuario(self, id_aluno: int) -> list[Review]:
        return (self.session.query(Review).filter_by(id_aluno=id_aluno).all())