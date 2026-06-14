from abc import ABC, abstractmethod

from core.entities.Review import Review


class IReviewRepository(ABC):

    @abstractmethod
    def salva(self, review: Review) -> None:
        pass

    @abstractmethod
    def encontra_por_materia(self, id_materia: int) -> list[Review]:
        pass

    @abstractmethod
    def encontra_por_usuario(self, id_aluno: int) -> list[Review]:
        pass