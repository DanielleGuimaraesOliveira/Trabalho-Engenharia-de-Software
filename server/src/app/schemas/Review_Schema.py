from typing import List

from pydantic import BaseModel

from src.core.entities.Review import Review

class ReviewSchema(BaseModel):
    """publicação de reviews."""

    comentario: str
    nota: int
    id_aluno: int
    id_materia: int

class ReviewBuscaSchema(BaseModel):
    """Busca review por id."""
    id: int

class ListagemReviewsSchema(BaseModel):
    """Listagem de reviews."""

    reviews: List[ReviewSchema]

def apresenta_reviews(reviews: List[Review]) -> dict:
    return {
        "reviews": [
            {
                "id": review.id,
                "comentario": review.comentario,
                "nota": review.nota,
                "id_aluno": review.id_aluno,
                "id_materia": review.id_materia
            }
            for review in reviews
        ]
    }

def apresenta_review(review):
    return {
        "id": review.id,
        "comentario": review.comentario,
        "nota": review.nota
    }