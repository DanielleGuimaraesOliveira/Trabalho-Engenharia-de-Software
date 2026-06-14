from src.core.entities.Aluno import Aluno
from src.core.entities.Materia import Materia


class Review:

    AVALIACAO_MINIMA = 1
    AVALIACAO_MAXIMA = 5

    def __init__(self, id: int, aluno: Aluno, materia: Materia, avaliacao: int, descricao: str =""):
        self.__validaAvaliacao(avaliacao)

        self.id = id
        self.aluno = aluno
        self.materia = materia
        self.avaliacao = avaliacao
        self.descricao = descricao

    def __validaAvaliacao(self, avaliacao: int):
        if avaliacao < self.AVALIACAO_MINIMA or avaliacao > self.AVALIACAO_MAXIMA:
            raise ValueError(
                f"A nota deve estar entre "
                f"{self.AVALIACAO_MINIMA} e {self.AVALIACAO_MAXIMA}"
            )
