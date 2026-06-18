from src.core.interfaces.IMateriaRepository import IMateriaRepository

class ListaMateriasUseCase:

    def __init__(self, repositorio_materia: IMateriaRepository):
        self.repositorio_materia = repositorio_materia

    def executa(self):
        return self.repositorio_materia.retorna_todas_as_materias()