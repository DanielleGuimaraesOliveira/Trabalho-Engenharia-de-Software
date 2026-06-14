from src.core.entities.Materia import Materia
from src.infra.db.model.materia_model import MateriaModel



class MateriaMapper:

    @staticmethod
    def to_model(materia: Materia) -> MateriaModel:
        return MateriaModel(nome=materia.nome, descricao=materia.descricao)

    @staticmethod
    def to_entity( model: MateriaModel) -> Materia:

        return Materia(id=model.id, nome=model.nome, descricao=model.descricao)