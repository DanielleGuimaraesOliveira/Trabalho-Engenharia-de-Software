from src.core.entities.Aluno import Aluno
from src.core.entities.Materia import Materia


class Review:

    NOTA_MINIMA = 1
    NOTA_MAXIMA = 5

    def __init__(self, id_aluno: int, id_materia: int, nota: int, comentario: str ="", id: int=0):
        self.__validaNota(nota)

        self.id = id
        self.id_aluno = id_aluno
        self.id_materia = id_materia
        self.nota = nota
        self.comentario = comentario

    def __validaNota(self, nota: int):
        if nota < self.NOTA_MINIMA or nota > self.NOTA_MAXIMA:
            raise ValueError(
                f"A nota deve estar entre "
                f"{self.NOTA_MINIMA} e {self.NOTA_MAXIMA}"
            )
