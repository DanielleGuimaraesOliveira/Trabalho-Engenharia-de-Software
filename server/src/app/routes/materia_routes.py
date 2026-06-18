from flask_openapi3 import Tag
from src.app.schemas.Materia_Schema import (ListagemMateriasSchema, apresenta_materias)

materia_tag = Tag(name="Materia", description="Listagem de matérias")

def register_materia_routes(app, lista_materias_use_case):

    @app.get("/materias",tags=[materia_tag], responses={"200": ListagemMateriasSchema})
    def lista_materias():
        materias = lista_materias_use_case.executa()

        return apresenta_materias(materias), 200