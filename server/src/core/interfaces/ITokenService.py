from abc import ABC, abstractmethod


class ITokenService(ABC):

    @abstractmethod
    def gerar_token(self, aluno_id: int) -> str:
        pass

    @abstractmethod
    def decodifica_token(self, token: str) -> int:
        """Retorna o id do aluno (sub) contido no token, ou lança exceção se inválido/expirado."""
        pass
