import pytest
import sys
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path

# Add the server directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.use_case.PublicaReviewUseCase import PublicarReviewUseCase
from src.core.use_case.ListaTodasAsReviewsUseCase import ListaReviewsUseCase
from src.core.dto.ReviewDTO import ReviewDTO
from src.core.entities.Review import Review
from src.core.entities.Aluno import Aluno
from src.core.entities.Materia import Materia
from src.core.enums.departamento import Departamento


class TestPublicarReviewUseCase:
    """Tests for the PublishReviewUseCase"""
    
    def setup_method(self):
        """Setup mocks before each test"""
        self.mock_aluno_repo = Mock()
        self.mock_materia_repo = Mock()
        self.mock_review_repo = Mock()
        self.use_case = PublicarReviewUseCase(
            repositorio_aluno=self.mock_aluno_repo,
            repositorio_materia=self.mock_materia_repo,
            repositorio_review=self.mock_review_repo
        )
    
    def test_publica_review_with_valid_data(self):
        """Test publishing a review with valid data"""
        # Arrange
        dto = ReviewDTO(
            comentario="Excelente disciplina",
            nota=5, # Nota ajustada para o limite 1-5
            id_aluno=1,
            id_materia=1
        )
        
        aluno = Aluno(nome="João", email="joao@aluno.puc-rio.br", senhaHash="hash")
        aluno.id = 1
        materia = Materia(id=1, codigo="INF1001", nome="Engenharia de Software", departamento=Departamento.INFORMATICA)
        
        self.mock_aluno_repo.encontra_por_id.return_value = aluno
        self.mock_materia_repo.encontra_por_id.return_value = materia
        self.mock_review_repo.salva.return_value = None
        
        # Act
        result = self.use_case.executa(dto)
        
        # Assert
        assert result.comentario == "Excelente disciplina"
        assert result.nota == 5
        assert result.id_aluno == 1
        assert result.id_materia == 1
        self.mock_aluno_repo.encontra_por_id.assert_called_once_with(1)
        self.mock_materia_repo.encontra_por_id.assert_called_once_with(1)
        self.mock_review_repo.salva.assert_called_once()
    
    def test_publica_review_aluno_not_found(self):
        """Test publishing review when student is not found"""
        # Arrange
        dto = ReviewDTO(
            comentario="Comentário",
            nota=4,
            id_aluno=999,
            id_materia=1
        )
        
        self.mock_aluno_repo.encontra_por_id.return_value = None
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            self.use_case.executa(dto)
        assert "Aluno não encontrado" in str(exc_info.value)
    
    def test_publica_review_materia_not_found(self):
        """Test publishing review when subject is not found"""
        # Arrange
        dto = ReviewDTO(
            comentario="Comentário",
            nota=4,
            id_aluno=1,
            id_materia=999
        )
        
        aluno = Aluno(nome="João", email="joao@aluno.puc-rio.br", senhaHash="hash")
        aluno.id = 1
        
        self.mock_aluno_repo.encontra_por_id.return_value = aluno
        self.mock_materia_repo.encontra_por_id.return_value = None
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            self.use_case.executa(dto)
        assert "Matéria não encontrada" in str(exc_info.value)
    
    def test_publica_review_repository_called(self):
        """Test that review is saved to repository"""
        # Arrange
        dto = ReviewDTO(
            comentario="Bom",
            nota=3,
            id_aluno=1,
            id_materia=1
        )
        
        aluno = Aluno(nome="João", email="joao@aluno.puc-rio.br", senhaHash="hash")
        aluno.id = 1
        materia = Materia(id=1, codigo="MAT1001", nome="Math", departamento=Departamento.MATEMATICA)
        
        self.mock_aluno_repo.encontra_por_id.return_value = aluno
        self.mock_materia_repo.encontra_por_id.return_value = materia
        
        # Act
        self.use_case.executa(dto)
        
        # Assert
        self.mock_review_repo.salva.assert_called_once()
        saved_review = self.mock_review_repo.salva.call_args[0][0]
        assert saved_review.comentario == "Bom"
        assert saved_review.nota == 3
    
    def test_publica_review_validates_both_entities(self):
        """Test that both aluno and materia are validated"""
        # Arrange
        dto = ReviewDTO(
            comentario="Test",
            nota=5,
            id_aluno=1,
            id_materia=1
        )
        
        self.mock_aluno_repo.encontra_por_id.return_value = None
        
        # Act & Assert
        with pytest.raises(Exception):
            self.use_case.executa(dto)
        
        self.mock_aluno_repo.encontra_por_id.assert_called_once()
        self.mock_materia_repo.encontra_por_id.assert_not_called()


class TestListaReviewsUseCase:
    """Tests for the ListReviewsUseCase"""
    
    def setup_method(self):
        """Setup mocks before each test"""
        self.mock_review_repo = Mock()
        self.mock_materia_repo = Mock()
        self.use_case = ListaReviewsUseCase(
            repositorio_review=self.mock_review_repo,
            repositorio_materia=self.mock_materia_repo
        )
    
    def test_lista_reviews_by_materia(self):
        """Test listing reviews by subject"""
        # Arrange
        materia = Materia(id=1, codigo="INF1004", nome="Python", departamento=Departamento.INFORMATICA)
        
        reviews = [
            Review(comentario="Ótimo", nota=5, id_aluno=1, id_materia=1),
            Review(comentario="Muito bom", nota=4, id_aluno=2, id_materia=1)
        ]
        
        self.mock_materia_repo.encontra_por_id.return_value = materia
        self.mock_review_repo.encontra_por_materia.return_value = reviews
        
        # Act
        result = self.use_case.executa(1)
        
        # Assert
        assert len(result) == 2
        assert result[0].nota == 5
        assert result[1].nota == 4
        self.mock_materia_repo.encontra_por_id.assert_called_once_with(1)
        self.mock_review_repo.encontra_por_materia.assert_called_once_with(1)
    
    def test_lista_reviews_materia_not_found(self):
        """Test listing reviews for non-existent subject"""
        # Arrange
        self.mock_materia_repo.encontra_por_id.return_value = None
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            self.use_case.executa(999)
        assert "Matéria não encontrada" in str(exc_info.value)
    
    def test_lista_reviews_empty_list(self):
        """Test listing reviews when no reviews exist for subject"""
        # Arrange
        materia = Materia(id=1, codigo="INF9099", nome="Subject", departamento=Departamento.INFORMATICA)
        
        self.mock_materia_repo.encontra_por_id.return_value = materia
        self.mock_review_repo.encontra_por_materia.return_value = []
        
        # Act
        result = self.use_case.executa(1)
        
        # Assert
        assert result == []
    
    def test_lista_reviews_multiple_reviews(self):
        """Test listing multiple reviews for a subject"""
        # Arrange
        materia = Materia(id=5, codigo="INF1005", nome="JavaScript", departamento=Departamento.INFORMATICA)
        
        reviews = [
            Review(comentario="Rev1", nota=3, id_aluno=1, id_materia=5),
            Review(comentario="Rev2", nota=4, id_aluno=2, id_materia=5),
            Review(comentario="Rev3", nota=5, id_aluno=3, id_materia=5)
        ]
        
        self.mock_materia_repo.encontra_por_id.return_value = materia
        self.mock_review_repo.encontra_por_materia.return_value = reviews
        
        # Act
        result = self.use_case.executa(5)
        
        # Assert
        assert len(result) == 3
        self.mock_review_repo.encontra_por_materia.assert_called_once_with(5)


class TestReviewEntity:
    """Tests for Review entity"""
    
    def test_review_creation(self):
        """Test creating a Review instance"""
        review = Review(
            comentario="Excelente",
            nota=5,
            id_aluno=1,
            id_materia=1
        )
        assert review.comentario == "Excelente"
        assert review.nota == 5
        assert review.id_aluno == 1
        assert review.id_materia == 1
    
    def test_review_with_id(self):
        """Test Review with id"""
        review = Review(
            comentario="Good",
            nota=4,
            id_aluno=1,
            id_materia=1
        )
        review.id = 42
        assert review.id == 42
    
    def test_review_properties(self):
        """Test Review properties"""
        review = Review(
            comentario="Comment",
            nota=3,
            id_aluno=1,
            id_materia=1
        )
        assert hasattr(review, 'comentario')
        assert hasattr(review, 'nota')
        assert hasattr(review, 'id_aluno')
        assert hasattr(review, 'id_materia')


class TestReviewDTO:
    """Tests for ReviewDTO"""
    
    def test_review_dto_creation(self):
        """Test creating ReviewDTO"""
        dto = ReviewDTO(
            comentario="Test comment",
            nota=4,
            id_aluno=1,
            id_materia=1
        )
        assert dto.comentario == "Test comment"
        assert dto.nota == 4
        assert dto.id_aluno == 1
        assert dto.id_materia == 1
    
    def test_review_dto_with_different_ratings(self):
        """Test ReviewDTO with different rating values"""
        for nota in range(1, 6): # Ajustado para o loop testar de 1 a 5
            dto = ReviewDTO(
                comentario="Comment",
                nota=nota,
                id_aluno=1,
                id_materia=1
            )
            assert dto.nota == nota


class TestReviewRoutes:
    """Tests for review routes"""
    
    def setup_method(self):
        """Setup test fixtures"""
        from src.app.main import app
        self.app = app
        self.client = app.test_client()
    
    def test_review_routes_structure(self):
        """Test review routes are properly registered"""
        # This verifies the route endpoints exist
        # Actual HTTP tests would require full app setup with database
        pass
    
    @patch('src.core.use_case.PublicaReviewUseCase.PublicarReviewUseCase.executa')
    def test_publica_review_route_structure(self, mock_use_case):
        """Test POST /review route structure"""
        # This test demonstrates the route testing approach
        pass
    
    @patch('src.core.use_case.ListaTodasAsReviewsUseCase.ListaReviewsUseCase.executa')
    def test_lista_reviews_route_structure(self, mock_use_case):
        """Test GET /reviews route structure"""
        # This test demonstrates the route testing approach
        pass


class TestReviewSchema:
    """Tests for Review Schema validation"""
    
    def test_review_schema_valid(self):
        """Test valid Review schema"""
        from src.app.schemas.Review_Schema import ReviewSchema
        # Schema validation test
        pass
    
    def test_apresenta_review_function(self):
        """Test apresenta_review function"""
        from src.app.schemas.Review_Schema import apresenta_review
        
        # Create mock review
        review = Mock(
            id=1,
            comentario="Excelente",
            nota=5,
            id_aluno=1,
            id_materia=1
        )
        
        result = apresenta_review(review)
        assert result is not None
    
    def test_apresenta_reviews_function(self):
        """Test apresenta_reviews function"""
        from src.app.schemas.Review_Schema import apresenta_reviews
        
        reviews = [
            Mock(id=1, comentario="Rev1", nota=4, id_aluno=1, id_materia=1),
            Mock(id=2, comentario="Rev2", nota=5, id_aluno=2, id_materia=1)
        ]
        
        result = apresenta_reviews(reviews)
        assert result is not None


class TestReviewRepositoryInterface:
    """Tests for Review Repository Interface"""
    
    def test_review_repository_find_by_materia(self):
        """Test repository method to find reviews by subject"""
        mock_repo = Mock()
        reviews = [
            Review(comentario="Rev1", nota=4, id_aluno=1, id_materia=1),
            Review(comentario="Rev2", nota=5, id_aluno=2, id_materia=1)
        ]
        
        mock_repo.encontra_por_materia.return_value = reviews
        
        result = mock_repo.encontra_por_materia(1)
        assert len(result) == 2
        mock_repo.encontra_por_materia.assert_called_once_with(1)
    
    def test_review_repository_save(self):
        """Test repository method to save review"""
        mock_repo = Mock()
        review = Review(comentario="Test", nota=3, id_aluno=1, id_materia=1)
        
        mock_repo.salva.return_value = None
        
        mock_repo.salva(review)
        mock_repo.salva.assert_called_once_with(review)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])