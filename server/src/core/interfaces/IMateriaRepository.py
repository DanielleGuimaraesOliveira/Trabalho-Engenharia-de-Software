from abc import ABC, abstractmethod

from src.core.entities.Materia import Materia


class IMateriaRepository(ABC):
    @abstractmethod
    def encontra_por_id(self, id_materia: int) -> Materia:
        pass

    @abstractmethod
    def retorna_todas_as_materias(self) -> list[Materia]:
        pass
