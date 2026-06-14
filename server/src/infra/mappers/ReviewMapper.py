from core.entities.Review import Review
from infra.db.model.review_model import ReviewModel



class ReviewMapper:

    @staticmethod
    def to_model(review: Review) -> ReviewModel:

        return ReviewModel(comentario = review.comentario, nota = review.nota, id_aluno = review.id_aluno, id_materia = review.id_materia)

    @staticmethod
    def to_entity( model: ReviewModel) -> Review:

        return Review( id=model.id, comentario=model.comentario, nota=model.nota, id_aluno=model.id_aluno, id_materia=model.id_materia)