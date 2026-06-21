import re
from src.core.enums.departamento import Departamento


class Materia:

    PADRAO_CODIGO = r"^[A-Z]{3}\d{4}$"

    def __init__(self, id: int, nome: str, codigo: str, departamento: str):
        self.__validaNome(nome)
        self.__validaCodigo(codigo)
        self.__validaDepartamento(departamento)

        self.id = id
        self.nome = nome
        self.codigo = codigo.upper()
        self.departamento = departamento

    def __validaNome(self, nome: str):
        if len(nome.strip()) < 3:
            raise ValueError("Nome da matéria inválido")

    def __validaCodigo(self, codigo: str):
        codigo = codigo.strip().upper()

        if not re.match(self.PADRAO_CODIGO, codigo):
            raise ValueError("O código deve seguir o padrão AAA0000")

    def __validaDepartamento(self, departamento: Departamento):
        if not isinstance(departamento, Departamento):
            raise ValueError("Departamento inválido")
