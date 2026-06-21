from src.core.interfaces.IMateriaRepository import IMateriaRepository


class ListaMateriaPorIdUseCase:

    def __init__(self, repositorio_materia: IMateriaRepository):
        self.repositorio_materia = repositorio_materia

    def executa(self, materia_id: int):

        materia = self.repositorio_materia.encontra_por_id(materia_id)

        if not materia:
            raise Exception("Matéria não encontrada")

        return materia
