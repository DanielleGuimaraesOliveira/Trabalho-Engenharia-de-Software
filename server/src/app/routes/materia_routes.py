from flask_openapi3 import Tag
from src.app.schemas.Materia_Schema import (
    ListagemMateriasSchema,
    MateriaSchema,
    MateriaBuscaPathSchema,
    apresenta_materias,
    apresenta_materia
)

materia_tag = Tag(name="Materia", description="Listagem de matérias")


def register_materia_routes(app, lista_materias_use_case, lista_materia_por_id_use_case):

    @app.get("/materias", tags=[materia_tag], responses={"200": ListagemMateriasSchema})
    def lista_materias():
        materias = lista_materias_use_case.executa()

        return apresenta_materias(materias), 200

    @app.get(
        "/materias/<int:materia_id>",
        tags=[materia_tag],
        responses={"200": MateriaSchema}
    )
    def busca_materia(path: MateriaBuscaPathSchema):
        try:
            materia = lista_materia_por_id_use_case.executa(path.materia_id)

            return apresenta_materia(materia), 200

        except Exception as error:
            return {"message": str(error)}, 404