class ReviewDTO:

    def __init__(self, comentario: str, nota: int, id_aluno: int, id_materia: int):
        self.comentario = comentario
        self.nota = nota
        self.id_aluno = id_aluno
        self.id_materia = id_materia