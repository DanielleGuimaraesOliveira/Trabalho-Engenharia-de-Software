from flask_openapi3 import Tag

from src.app.schemas import (
    ErrorSchema,
    ReviewSchema,
    ListagemReviewsSchema,
    ReviewViewSchema,
    apresenta_review,
    apresenta_reviews
)
from src.core.dto.ReviewDTO import ReviewDTO
from src.core.use_case.PublicaReviewUseCase import PublicaReviewUseCase
from src.core.use_case.ListaTodasAsReviewsUseCase import ListaTodasAsReviewsUseCase

review_tag = Tag(name="Review", description="Publicação e listagem de reviews")

def register_review_routes(app, publica_use_case: PublicaReviewUseCase, lista_use_case: ListaTodasAsReviewsUseCase):
    @app.post("/review", tags=[review_tag], responses={ "200": ReviewViewSchema, "400": ErrorSchema})
    def publica_review(form: ReviewSchema):
        try:
            dto = ReviewDTO(comentario=form.comentario, nota=form.nota, id_aluno=form.id_aluno, id_materia=form.id_materia)
            review = publica_use_case.executa(dto)

            return apresenta_review(review), 200

        except Exception as error:
            return {"message": str(error)}, 400

    @app.get("/reviews", tags=[review_tag], responses={ "200": ListagemReviewsSchema})
    def lista_reviews():
        reviews = lista_use_case.executa()

        if not reviews:
            return {"reviews": []}, 200
        
        return apresenta_reviews(reviews), 200