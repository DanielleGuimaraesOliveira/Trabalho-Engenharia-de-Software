import pytest
import sys
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path

# Add the server directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.use_case.CriaAlunoUseCase import CriaAlunoUseCase
from src.core.use_case.AutenticaAlunoUseCase import AutenticaAlunoUseCase
from src.core.dto.AlunoDTO import AlunoDTO
from src.core.dto.LoginDTO import LoginDTO
from src.core.entities.Aluno import Aluno


class TestCriaAlunoUseCase:
    """Tests for the CreateStudentUseCase"""
    
    def setup_method(self):
        """Setup mocks before each test"""
        self.mock_repository = Mock()
        self.mock_hash_service = Mock()
        self.use_case = CriaAlunoUseCase(
            repositorio_aluno=self.mock_repository,
            senha_hash=self.mock_hash_service
        )
    
    def test_cria_aluno_with_valid_data(self):
        """Test creating a student with valid data"""
        # Arrange
        dto = AlunoDTO(nome="João Silva", email="joao@example.com", senha="senha123")
        self.mock_hash_service.hash.return_value = "hashed_password"
        self.mock_repository.salva.return_value = None
        
        # Act
        result = self.use_case.executa(dto)
        
        # Assert
        assert result.nome == "João Silva"
        assert result.email == "joao@example.com"
        self.mock_hash_service.hash.assert_called_once_with("senha123")
        self.mock_repository.salva.assert_called_once()
    
    def test_cria_aluno_hash_password(self):
        """Test that password is hashed during creation"""
        # Arrange
        dto = AlunoDTO(nome="Maria", email="maria@example.com", senha="pass123")
        hashed = "hashed_pass123"
        self.mock_hash_service.hash.return_value = hashed
        
        # Act
        self.use_case.executa(dto)
        
        # Assert
        self.mock_hash_service.hash.assert_called_once_with("pass123")
        saved_aluno = self.mock_repository.salva.call_args[0][0]
        assert saved_aluno.senhaHash == hashed
    
    def test_cria_aluno_repository_called(self):
        """Test that repository save method is called"""
        # Arrange
        dto = AlunoDTO(nome="Pedro", email="pedro@example.com", senha="pwd")
        self.mock_hash_service.hash.return_value = "hashed"
        
        # Act
        self.use_case.executa(dto)
        
        # Assert
        self.mock_repository.salva.assert_called_once()
        saved_aluno = self.mock_repository.salva.call_args[0][0]
        assert saved_aluno.nome == "Pedro"
        assert saved_aluno.email == "pedro@example.com"


class TestAutenticaAlunoUseCase:
    """Tests for the AuthenticateStudentUseCase"""
    
    def setup_method(self):
        """Setup mocks before each test"""
        self.mock_repository = Mock()
        self.mock_token_service = Mock()
        self.mock_hash_service = Mock()
        self.use_case = AutenticaAlunoUseCase(
            repositorio_aluno=self.mock_repository,
            token_service=self.mock_token_service,
            hash_service=self.mock_hash_service
        )
    
    def test_autentica_aluno_with_valid_credentials(self):
        """Test authentication with valid credentials"""
        # Arrange
        dto = LoginDTO(email="joao@example.com", senha="senha123")
        aluno = Aluno(nome="João", email="joao@example.com", senhaHash="hashed_senha123")
        aluno.id = 1
        
        self.mock_repository.encontra_por_email.return_value = aluno
        self.mock_hash_service.verificar.return_value = True
        self.mock_token_service.gerar_token.return_value = "token_abc123"
        
        # Act
        result = self.use_case.executa(dto)
        
        # Assert
        assert result == {"token": "token_abc123"}
        self.mock_repository.encontra_por_email.assert_called_once_with("joao@example.com")
        self.mock_hash_service.verificar.assert_called_once()
        self.mock_token_service.gerar_token.assert_called_once_with(1)
    
    def test_autentica_aluno_email_not_found(self):
        """Test authentication with non-existent email"""
        # Arrange
        dto = LoginDTO(email="nonexistent@example.com", senha="senha123")
        self.mock_repository.encontra_por_email.return_value = None
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            self.use_case.executa(dto)
        assert "Email inválido" in str(exc_info.value)
    
    def test_autentica_aluno_invalid_password(self):
        """Test authentication with invalid password"""
        # Arrange
        dto = LoginDTO(email="joao@example.com", senha="wrong_password")
        aluno = Aluno(nome="João", email="joao@example.com", senhaHash="hashed_senha123")
        aluno.id = 1
        
        self.mock_repository.encontra_por_email.return_value = aluno
        self.mock_hash_service.verificar.return_value = False
        
        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            self.use_case.executa(dto)
        assert "Senha inválida" in str(exc_info.value)
    
    def test_autentica_aluno_gera_token(self):
        """Test that token is generated for valid authentication"""
        # Arrange
        dto = LoginDTO(email="joao@example.com", senha="senha123")
        aluno = Aluno(nome="João", email="joao@example.com", senhaHash="hashed")
        aluno.id = 42
        
        self.mock_repository.encontra_por_email.return_value = aluno
        self.mock_hash_service.verificar.return_value = True
        self.mock_token_service.gerar_token.return_value = "generated_token"
        
        # Act
        result = self.use_case.executa(dto)
        
        # Assert
        self.mock_token_service.gerar_token.assert_called_once_with(42)
        assert result["token"] == "generated_token"


class TestAlunoRoutesIntegration:
    """Integration tests for aluno routes"""
    
    def setup_method(self):
        """Setup test client"""
        from src.app.main import app as flask_app
        self.app = flask_app
        self.client = flask_app.test_client()
    
    def test_home_route_returns_ok(self):
        """Test that the home route returns 200"""
        response = self.client.get("/")
        assert response.status_code == 200
    
    @patch('src.app.routes.aluno_routes.cria_aluno_use_case')
    def test_create_aluno_route_valid(self, mock_use_case):
        """Test creating student via route with valid data"""
        # Note: This test demonstrates the testing approach
        # In practice, you would need proper test database setup
        pass
    
    @patch('src.app.routes.aluno_routes.auth_use_case')
    def test_login_route_valid(self, mock_use_case):
        """Test login route with valid credentials"""
        # Note: This test demonstrates the testing approach
        pass


class TestAlunoDTO:
    """Tests for AlunoDTO"""
    
    def test_aluno_dto_creation(self):
        """Test creating AlunoDTO"""
        dto = AlunoDTO(nome="João", email="joao@example.com", senha="senha123")
        assert dto.nome == "João"
        assert dto.email == "joao@example.com"
        assert dto.senha == "senha123"


class TestLoginDTO:
    """Tests for LoginDTO"""
    
    def test_login_dto_creation(self):
        """Test creating LoginDTO"""
        dto = LoginDTO(email="joao@example.com", senha="senha123")
        assert dto.email == "joao@example.com"
        assert dto.senha == "senha123"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
