from abc import ABC, abstractmethod


class IAlunoRepository(ABC):

    @abstractmethod
    def salva(self, aluno):
        pass

    @abstractmethod
    def encontra_por_id(self, id: int):
        pass

    @abstractmethod
    def encontra_por_email(self, email: str):
        pass
