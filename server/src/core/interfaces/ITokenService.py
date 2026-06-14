from abc import ABC, abstractmethod

class ITokenService(ABC):

    @abstractmethod
    def gerar_token(self, aluno_id: int) -> str:
        pass