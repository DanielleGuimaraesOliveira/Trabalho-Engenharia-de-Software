from core.entities.Review import Review
from core.interfaces.IAlunoRepository import IAlunoRepository
from core.interfaces.IReviewRepository import IReviewRepository
from core.interfaces.IMateriaRepository import IMateriaRepository

class PublicarReviewUserCase:

    def __init__(self, repositorio_aluno: IAlunoRepository, repositorio_materia: IMateriaRepository, repositorio_review: IReviewRepository):
        self.repositorio_aluno = repositorio_aluno
        self.repositorio_materia = repositorio_materia
        self.repositorio_review = repositorio_review

    def executa(self, dto):
        aluno = self.repositorio_aluno.encontra_por_id(dto.id_aluno)

        if not aluno:
            raise Exception("Aluno não encontrado")

        materia = self.repositorio_materia.encontra_por_id(dto.id_materia)

        if not materia:
            raise Exception("Matéria não encontrada")

        review = Review(comentario=dto.comentario, nota = dto.nota, id_aluno = dto.id_aluno, id_materia = dto.id_materia)

        self.repositorio_review.salva(review)