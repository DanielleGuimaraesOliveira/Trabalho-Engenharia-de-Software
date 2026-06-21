from src.core.interfaces.IReviewRepository import IReviewRepository
from src.core.interfaces.IMateriaRepository import IMateriaRepository
from src.core.interfaces.IAlunoRepository import IAlunoRepository


class ListaReviewsUseCase:

    def __init__(
        self,
        repositorio_review: IReviewRepository,
        repositorio_materia: IMateriaRepository,
        repositorio_aluno: IAlunoRepository
    ):

        self.repositorio_review = repositorio_review
        self.repositorio_materia = repositorio_materia
        self.repositorio_aluno = repositorio_aluno

    def executa(self, materia_id: int):

        materia = self.repositorio_materia.encontra_por_id(materia_id)

        if not materia:
            raise Exception("Matéria não encontrada")

        reviews = self.repositorio_review.encontra_por_materia(materia_id)

        for review in reviews:
            aluno = self.repositorio_aluno.encontra_por_id(review.id_aluno)
            review.nome_aluno = aluno.nome if aluno else "Aluno"

        return reviews