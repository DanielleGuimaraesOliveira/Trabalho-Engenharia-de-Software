from pydantic import BaseModel

class AlunoSchema(BaseModel):
    nome: str
    email: str
    senha: str