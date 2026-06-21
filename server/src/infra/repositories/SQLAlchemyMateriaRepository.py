from src.core.entities.Materia import Materia
from src.core.interfaces.IMateriaRepository import IMateriaRepository
from src.infra.db.model.materia_model import MateriaModel
from src.infra.mappers.MateriaMapper import MateriaMapper


class SQLAlchemyMateriaRepositorio(IMateriaRepository):
    def __init__(self, session):
        self.session = session

    def salva(self, materia: Materia) -> bool:
        model = MateriaMapper.to_model(materia)

        self.session.add(model)
        self.session.commit()

        return True

    def encontra_por_id(self, id: int) -> Materia:
        model = self.session.query(MateriaModel).filter_by(id=id).first()

        if not model:
            return None

        return MateriaMapper.to_entity(model)

    def encontra_por_nome(self, nome: str) -> Materia:
        model = self.session.query(MateriaModel).filter_by(nome=nome).first()

        if not model:
            return None

        return MateriaMapper.to_entity(model)

    def retorna_todas_as_materias(self) -> list[Materia]:

        models = self.session.query(MateriaModel).all()

        return [MateriaMapper.to_entity(model) for model in models]
