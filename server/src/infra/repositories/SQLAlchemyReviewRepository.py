from src.core.entities.Review import Review
from src.core.interfaces.IReviewRepository import IReviewRepository
from src.infra.db.model.review_model import ReviewModel
from src.infra.mappers.ReviewMapper import ReviewMapper


class SQLAlchemyReviewRepositorio(IReviewRepository):
    def __init__(self, session):
        self.session = session

    def salva(self, review: Review) -> bool:
        model = ReviewMapper.to_model(review)

        self.session.add(model)
        self.session.commit()

        return True

    def encontra_por_id(self, id: int) -> Review:

        model = self.session.query(ReviewModel).filter_by(id=id).first()

        if not model:
            return None

        return ReviewMapper.to_entity(model)

    def encontra_por_materia(self, id_materia: int) -> list[Review]:
        models = self.session.query(ReviewModel).filter_by(
            id_materia=id_materia).all()

        return [ReviewMapper.to_entity(model) for model in models]

    def encontra_por_aluno(self, id_aluno: int) -> list[Review]:
        models = self.session.query(
            ReviewModel).filter_by(id_aluno=id_aluno).all()

        return [ReviewMapper.to_entity(model) for model in models]
