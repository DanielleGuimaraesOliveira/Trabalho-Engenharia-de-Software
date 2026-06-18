from src.core.dto.ReviewDTO import ReviewDTO
from src.core.interfaces.IReviewRepository import IReviewRepository
from src.core.interfaces.IMateriaRepository import IMateriaRepository


class ListaReviewsUseCase:

    def __init__(
        self,
        repositorio_review: IReviewRepository,
        repositorio_materia: IMateriaRepository
    ):

        self.repositorio_review = repositorio_review
        self.repositorio_materia = repositorio_materia

    def executa(self, materia_id: int):

        materia = self.repositorio_materia.encontra_por_id(materia_id)

        if not materia:
            raise Exception("Matéria não encontrada")

        return self.repositorio_review.encontra_por_materia(materia_id)