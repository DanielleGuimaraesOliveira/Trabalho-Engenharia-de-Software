from flask_openapi3 import Tag

from src.app.schemas import (
    ErrorSchema,
    ReviewSchema,
    ListagemReviewsSchema,
    ReviewViewSchema,
    ReviewBuscaSchema,
    apresenta_review,
    apresenta_reviews
)
from src.core.dto.ReviewDTO import ReviewDTO
from src.core.use_case.PublicaReviewUseCase import PublicarReviewUseCase
from src.core.use_case.ListaTodasAsReviewsUseCase import ListaReviewsUseCase

review_tag = Tag(name="Review", description="Publicação e listagem de reviews")

def register_review_routes(app, publica_use_case: PublicarReviewUseCase, lista_use_case: ListaReviewsUseCase):
    @app.post("/review", tags=[review_tag], responses={ "200": ReviewViewSchema, "400": ErrorSchema})
    def publica_review(body: ReviewSchema):
        try:
            dto = ReviewDTO(comentario=body.comentario, nota=body.nota, id_aluno=body.id_aluno, id_materia=body.id_materia)
            review = publica_use_case.executa(dto)

            return apresenta_review(review), 200

        except Exception as error:
            return {"message": str(error)}, 400

    @app.get("/reviews", tags=[review_tag], responses={"200": ListagemReviewsSchema})
    def lista_reviews(query: ReviewBuscaSchema):

        reviews = (lista_use_case.executa(query.materia_id))

        if not reviews:
            return {"reviews": []}, 200

        return apresenta_reviews(reviews), 200