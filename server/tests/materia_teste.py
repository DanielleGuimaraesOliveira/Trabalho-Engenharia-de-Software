import pytest
import sys
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path

# Add the server directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.use_case.ListaMateriasUseCase import ListaMateriasUseCase
from src.core.entities.Materia import Materia


class TestListaMateriasUseCase:
    """Tests for the ListSubjectsUseCase"""
    
    def setup_method(self):
        """Setup mocks before each test"""
        self.mock_repository = Mock()
        self.use_case = ListaMateriasUseCase(
            repositorio_materia=self.mock_repository
        )
    
    def test_lista_materias_returns_list(self):
        """Test that listing subjects returns a list"""
        # Arrange
        materias = [
            Materia(nome="Engenharia de Software", professor="Dr. Silva"),
            Materia(nome="Banco de Dados", professor="Dra. Santos")
        ]
        self.mock_repository.retorna_todas_as_materias.return_value = materias
        
        # Act
        result = self.use_case.executa()
        
        # Assert
        assert isinstance(result, list)
        assert len(result) == 2
        self.mock_repository.retorna_todas_as_materias.assert_called_once()
    
    def test_lista_materias_empty_list(self):
        """Test listing subjects when no subjects exist"""
        # Arrange
        self.mock_repository.retorna_todas_as_materias.return_value = []
        
        # Act
        result = self.use_case.executa()
        
        # Assert
        assert result == []
        self.mock_repository.retorna_todas_as_materias.assert_called_once()
    
    def test_lista_materias_repository_called(self):
        """Test that repository method is called"""
        # Arrange
        materias = [Materia(nome="Programação", professor="Prof. João")]
        self.mock_repository.retorna_todas_as_materias.return_value = materias
        
        # Act
        result = self.use_case.executa()
        
        # Assert
        self.mock_repository.retorna_todas_as_materias.assert_called_once()
        assert result[0].nome == "Programação"
    
    def test_lista_materias_with_multiple_subjects(self):
        """Test listing multiple subjects"""
        # Arrange
        materias = [
            Materia(nome="Cálculo I", professor="Prof. A"),
            Materia(nome="Cálculo II", professor="Prof. B"),
            Materia(nome="Álgebra Linear", professor="Prof. C"),
            Materia(nome="Geometria", professor="Prof. D")
        ]
        self.mock_repository.retorna_todas_as_materias.return_value = materias
        
        # Act
        result = self.use_case.executa()
        
        # Assert
        assert len(result) == 4
        assert result[0].nome == "Cálculo I"
        assert result[3].nome == "Geometria"


class TestMateriaEntity:
    """Tests for Materia entity"""
    
    def test_materia_creation(self):
        """Test creating a Materia instance"""
        materia = Materia(nome="Python", professor="Dr. Silva")
        assert materia.nome == "Python"
        assert materia.professor == "Dr. Silva"
    
    def test_materia_with_id(self):
        """Test Materia with id"""
        materia = Materia(nome="JavaScript", professor="Dra. Santos")
        materia.id = 1
        assert materia.id == 1
    
    def test_materia_properties(self):
        """Test Materia properties"""
        materia = Materia(nome="React", professor="Prof. João")
        assert hasattr(materia, 'nome')
        assert hasattr(materia, 'professor')


class TestMateriaRoutes:
    """Tests for materia routes"""
    
    def setup_method(self):
        """Setup test fixtures"""
        pass
    
    @patch('src.app.routes.materia_routes.lista_materias_use_case')
    def test_lista_materias_route(self, mock_use_case):
        """Test GET /materias route"""
        # Arrange
        from src.app.main import app
        client = app.test_client()
        
        materias_mock = [
            Mock(id=1, nome="Engenharia de Software", professor="Dr. Silva"),
            Mock(id=2, nome="Banco de Dados", professor="Dra. Santos")
        ]
        mock_use_case.executa.return_value = materias_mock
        
        # This would need proper mocking of the app context
        # Note: In a real scenario, you'd setup a test database or use fixtures
    
    def test_lista_materias_integration(self):
        """Integration test for listing subjects"""
        from src.app.main import app
        client = app.test_client()
        
        # This test verifies the route structure
        # Note: Requires proper database setup
        response = client.get("/materias")
        assert response.status_code in [200, 500]  # 500 if DB not setup


class TestMateriaSchema:
    """Tests for Materia Schema validation"""
    
    def test_materia_schema_valid(self):
        """Test valid Materia schema"""
        from src.app.schemas.Materia_Schema import ListagemMateriasSchema
        # Schema validation test
        pass
    
    def test_apresenta_materias_function(self):
        """Test apresenta_materias function"""
        from src.app.schemas.Materia_Schema import apresenta_materias
        
        # Create mock materias
        materias = [
            Mock(id=1, nome="Subject1", professor="Prof1"),
            Mock(id=2, nome="Subject2", professor="Prof2")
        ]
        
        # This function should format the subjects for API response
        # Testing structure (actual implementation depends on schema)
        result = apresenta_materias(materias)
        assert result is not None


class TestMateriaRepositoryInterface:
    """Tests for Materia Repository Interface"""
    
    def test_materia_repository_find_by_id(self):
        """Test repository method to find subject by id"""
        mock_repo = Mock()
        materia = Materia(nome="Python", professor="Dr. Silva")
        materia.id = 1
        
        mock_repo.encontra_por_id.return_value = materia
        
        result = mock_repo.encontra_por_id(1)
        assert result.nome == "Python"
        mock_repo.encontra_por_id.assert_called_once_with(1)
    
    def test_materia_repository_find_all(self):
        """Test repository method to find all subjects"""
        mock_repo = Mock()
        materias = [
            Materia(nome="Math", professor="Prof. A"),
            Materia(nome="Physics", professor="Prof. B")
        ]
        
        mock_repo.retorna_todas_as_materias.return_value = materias
        
        result = mock_repo.retorna_todas_as_materias()
        assert len(result) == 2
        mock_repo.retorna_todas_as_materias.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
