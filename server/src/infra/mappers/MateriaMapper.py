from src.core.entities.Materia import Materia
from src.core.enums.departamento import Departamento
from src.infra.db.model.materia_model import MateriaModel


class MateriaMapper:

    @staticmethod
    def to_model(materia: Materia) -> MateriaModel:
        return MateriaModel(
            nome=materia.nome,
            codigo=materia.codigo,
            departamento=materia.departamento.name
        )

    @staticmethod
    def to_entity(model: MateriaModel) -> Materia:
        return Materia(
            id=model.id,
            nome=model.nome,
            codigo=model.codigo,
            departamento=Departamento[model.departamento]
        )