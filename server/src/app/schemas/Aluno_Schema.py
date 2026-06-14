from pydantic import BaseModel

class AlunoSchema(BaseModel):
    nome: str
    email: str
    senha: str
    
class AlunoViewSchema(BaseModel):
    id: int
    nome: str
    email: str