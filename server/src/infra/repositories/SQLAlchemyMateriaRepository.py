from core.entities.Materia import Materia
from core.interfaces.IMateriaRepository import IMateriaRepository


class SQLAlchemyMateriaRepositorio(IMateriaRepository):
    def __init__(self, session):
        self.session = session

    def encontra_por_id(self,id_materia: int) -> Materia:
        return (self.session.query(Materia).filter_by(id=id_materia).first())

    def retorna_todas_as_materias(self) -> list[Materia]:
        return (self.session.query(Materia).all()
        )