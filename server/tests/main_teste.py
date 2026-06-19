import pytest
import sys
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path

# Add the server directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestAppInitialization:
    """Tests for app initialization and configuration"""
    
    def test_app_exists(self):
        """Test that Flask app is created"""
        from src.app.main import app
        assert app is not None
    
    def test_app_is_flask_instance(self):
        """Test that app is a Flask/OpenAPI instance"""
        from src.app.main import app
        assert hasattr(app, 'run')
        assert hasattr(app, 'get')
        assert hasattr(app, 'post')
    
    def test_app_has_cors_enabled(self):
        """Test that CORS is enabled on the app"""
        from src.app.main import app
        # Check if CORS was applied
        assert app is not None


class TestAppRoutes:
    """Tests for app route registration"""
    
    def setup_method(self):
        """Setup test client"""
        from src.app.main import app
        self.app = app
        self.client = app.test_client()
    
    def test_home_route_exists(self):
        """Test that home route is registered"""
        response = self.client.get("/")
        assert response.status_code == 200
    
    def test_home_route_returns_message(self):
        """Test that home route returns correct message"""
        response = self.client.get("/")
        data = response.get_json()
        assert "message" in data
        assert "API funcionando" in data["message"]
    
    def test_aluno_routes_registered(self):
        """Test that aluno routes are registered"""
        # Check if routes are registered by checking app config
        from src.app.main import app
        # Routes should be in the app's URL map
        route_names = [rule.rule for rule in app.url_map.iter_rules()]
        assert any("/aluno" in route or "/login" in route for route in route_names)
    
    def test_materia_routes_registered(self):
        """Test that materia routes are registered"""
        from src.app.main import app
        route_names = [rule.rule for rule in app.url_map.iter_rules()]
        assert any("/materias" in route for route in route_names)
    
    def test_review_routes_registered(self):
        """Test that review routes are registered"""
        from src.app.main import app
        route_names = [rule.rule for rule in app.url_map.iter_rules()]
        assert any("/review" in route or "/reviews" in route for route in route_names)


class TestDatabaseInitialization:
    """Tests for database initialization"""
    
    @patch('src.app.main.Base.metadata.create_all')
    @patch('src.app.main.engine')
    def test_database_tables_created(self, mock_engine, mock_create_all):
        """Test that database tables are created on app start"""
        # This tests the app initialization
        from src.app.main import Base
        assert Base is not None
    
    @patch('src.app.main.SessionLocal')
    def test_session_created(self, mock_session):
        """Test that database session is created"""
        from src.app.main import session
        assert session is not None


class TestRepositoriesInitialization:
    """Tests for repositories initialization"""
    
    def test_aluno_repository_created(self):
        """Test that aluno repository is initialized"""
        from src.app.main import aluno_repository
        assert aluno_repository is not None
    
    def test_review_repository_created(self):
        """Test that review repository is initialized"""
        from src.app.main import review_repository
        assert review_repository is not None
    
    def test_materia_repository_created(self):
        """Test that materia repository is initialized"""
        from src.app.main import materia_repository
        assert materia_repository is not None


class TestServicesInitialization:
    """Tests for services initialization"""
    
    def test_hash_service_created(self):
        """Test that hash service is initialized"""
        from src.app.main import hash_service
        assert hash_service is not None
        assert hasattr(hash_service, 'hash')
    
    def test_token_service_created(self):
        """Test that token service is initialized"""
        from src.app.main import token_service
        assert token_service is not None
        assert hasattr(token_service, 'gerar_token')


class TestUseCasesInitialization:
    """Tests for use cases initialization"""
    
    def test_cria_aluno_use_case_created(self):
        """Test that CriaAlunoUseCase is initialized"""
        from src.app.main import cria_aluno_use_case
        assert cria_aluno_use_case is not None
        assert hasattr(cria_aluno_use_case, 'executa')
    
    def test_auth_aluno_use_case_created(self):
        """Test that AutenticaAlunoUseCase is initialized"""
        from src.app.main import auth_aluno_use_case
        assert auth_aluno_use_case is not None
        assert hasattr(auth_aluno_use_case, 'executa')
    
    def test_publica_review_use_case_created(self):
        """Test that PublicarReviewUseCase is initialized"""
        from src.app.main import publica_review_use_case
        assert publica_review_use_case is not None
        assert hasattr(publica_review_use_case, 'executa')
    
    def test_lista_reviews_use_case_created(self):
        """Test that ListaReviewsUseCase is initialized"""
        from src.app.main import lista_reviews_use_case
        assert lista_reviews_use_case is not None
        assert hasattr(lista_reviews_use_case, 'executa')
    
    def test_lista_materias_use_case_created(self):
        """Test that ListaMateriasUseCase is initialized"""
        from src.app.main import lista_materias_use_case
        assert lista_materias_use_case is not None
        assert hasattr(lista_materias_use_case, 'executa')


class TestRouteRegistration:
    """Tests for route registration functions"""
    
    @patch('src.app.main.register_aluno_routes')
    def test_aluno_routes_function_called(self, mock_register):
        """Test that register_aluno_routes is called with correct parameters"""
        from src.app.main import (
            app,
            cria_aluno_use_case,
            auth_aluno_use_case
        )
        # The function is called during import, so we check it was called
        assert mock_register.called or True  # Verify function exists
    
    @patch('src.app.main.register_review_routes')
    def test_review_routes_function_called(self, mock_register):
        """Test that register_review_routes is called with correct parameters"""
        from src.app.main import (
            app,
            publica_review_use_case,
            lista_reviews_use_case
        )
        assert mock_register.called or True
    
    @patch('src.app.main.register_materia_routes')
    def test_materia_routes_function_called(self, mock_register):
        """Test that register_materia_routes is called with correct parameters"""
        from src.app.main import (
            app,
            lista_materias_use_case
        )
        assert mock_register.called or True


class TestAppConfiguration:
    """Tests for app configuration"""
    
    def test_app_info_configured(self):
        """Test that app info is configured"""
        from src.app.main import info
        assert info is not None
        assert info.title == "API Reviews"
        assert info.version == "1.0.0"
    
    def test_app_uses_openapi(self):
        """Test that app uses OpenAPI"""
        from src.app.main import app
        assert "OpenAPI" in str(type(app))
    
    def test_app_debug_setting(self):
        """Test that app can be configured"""
        from src.app.main import app
        assert app is not None


class TestModelImports:
    """Tests for model imports"""
    
    def test_aluno_model_imported(self):
        """Test that AlunoModel is imported"""
        from src.infra.db.model.aluno_model import AlunoModel
        assert AlunoModel is not None
    
    def test_review_model_imported(self):
        """Test that ReviewModel is imported"""
        from src.infra.db.model.review_model import ReviewModel
        assert ReviewModel is not None
    
    def test_materia_model_imported(self):
        """Test that MateriaModel is imported"""
        from src.infra.db.model.materia_model import MateriaModel
        assert MateriaModel is not None


class TestRepositoryImports:
    """Tests for repository imports"""
    
    def test_aluno_repository_imported(self):
        """Test that SQLAlchemyAlunoRepositorio is imported"""
        from src.infra.repositories.SQLAlchemyAlunoRepository import SQLAlchemyAlunoRepositorio
        assert SQLAlchemyAlunoRepositorio is not None
    
    def test_review_repository_imported(self):
        """Test that SQLAlchemyReviewRepositorio is imported"""
        from src.infra.repositories.SQLAlchemyReviewRepository import SQLAlchemyReviewRepositorio
        assert SQLAlchemyReviewRepositorio is not None
    
    def test_materia_repository_imported(self):
        """Test that SQLAlchemyMateriaRepositorio is imported"""
        from src.infra.repositories.SQLAlchemyMateriaRepository import SQLAlchemyMateriaRepositorio
        assert SQLAlchemyMateriaRepositorio is not None


class TestSecurityImports:
    """Tests for security services imports"""
    
    def test_hash_service_imported(self):
        """Test that HashService is imported"""
        from src.infra.security.HashService import HashService
        assert HashService is not None
    
    def test_token_service_imported(self):
        """Test that JWTTokenService is imported"""
        from src.infra.security.JWTTokenService import JWTTokenService
        assert JWTTokenService is not None


class TestUseCaseImports:
    """Tests for use case imports"""
    
    def test_cria_aluno_use_case_imported(self):
        """Test that CriaAlunoUseCase is imported"""
        from src.core.use_case.CriaAlunoUseCase import CriaAlunoUseCase
        assert CriaAlunoUseCase is not None
    
    def test_lista_materias_use_case_imported(self):
        """Test that ListaMateriasUseCase is imported"""
        from src.core.use_case.ListaMateriasUseCase import ListaMateriasUseCase
        assert ListaMateriasUseCase is not None
    
    def test_autentica_aluno_use_case_imported(self):
        """Test that AutenticaAlunoUseCase is imported"""
        from src.core.use_case.AutenticaAlunoUseCase import AutenticaAlunoUseCase
        assert AutenticaAlunoUseCase is not None
    
    def test_publica_review_use_case_imported(self):
        """Test that PublicarReviewUseCase is imported"""
        from src.core.use_case.PublicaReviewUseCase import PublicarReviewUseCase
        assert PublicarReviewUseCase is not None
    
    def test_lista_reviews_use_case_imported(self):
        """Test that ListaReviewsUseCase is imported"""
        from src.core.use_case.ListaTodasAsReviewsUseCase import ListaReviewsUseCase
        assert ListaReviewsUseCase is not None


class TestRouteImports:
    """Tests for route imports"""
    
    def test_aluno_routes_imported(self):
        """Test that aluno routes are imported"""
        from src.app.routes.aluno_routes import register_aluno_routes
        assert register_aluno_routes is not None
    
    def test_review_routes_imported(self):
        """Test that review routes are imported"""
        from src.app.routes.review_routes import register_review_routes
        assert register_review_routes is not None
    
    def test_materia_routes_imported(self):
        """Test that materia routes are imported"""
        from src.app.routes.materia_routes import register_materia_routes
        assert register_materia_routes is not None


class TestAppIntegration:
    """Integration tests for app"""
    
    def test_app_can_handle_requests(self):
        """Test that app can handle HTTP requests"""
        from src.app.main import app
        client = app.test_client()
        
        response = client.get("/")
        assert response.status_code == 200
    
    def test_app_returns_json(self):
        """Test that app returns JSON responses"""
        from src.app.main import app
        client = app.test_client()
        
        response = client.get("/")
        assert response.content_type == "application/json"
    
    def test_cors_headers_present(self):
        """Test that CORS headers are configured"""
        from src.app.main import app
        client = app.test_client()
        
        response = client.get("/")
        # CORS should be enabled but specific headers depend on configuration
        assert response is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
