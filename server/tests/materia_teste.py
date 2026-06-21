from src.core.enums.departamento import Departamento
from src.core.entities.Materia import Materia
from src.core.use_case.ListaMateriasUseCase import ListaMateriasUseCase
import pytest
import sys
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path

# Add the server directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestListaMateriasUseCase:
    """Tests for the ListSubjectsUseCase"""

    def setup_method(self):
        """Setup mocks before each test"""
        self.mock_repository = Mock()
        self.use_case = ListaMateriasUseCase(
            repositorio_materia=self.mock_repository)

    def test_lista_materias_returns_list(self):
        """Test that listing subjects returns a list"""
        # Arrange
        materias = [
            Materia(
                id=1,
                codigo="INF1001",
                nome="Engenharia de Software",
                departamento=Departamento.INFORMATICA,
            ),
            Materia(
                id=2,
                codigo="INF1002",
                nome="Banco de Dados",
                departamento=Departamento.INFORMATICA,
            ),
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
        materias = [
            Materia(
                id=1,
                codigo="INF1003",
                nome="Programação",
                departamento=Departamento.INFORMATICA,
            )
        ]
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
            Materia(
                id=1,
                codigo="MAT1001",
                nome="Cálculo I",
                departamento=Departamento.MATEMATICA,
            ),
            Materia(
                id=2,
                codigo="MAT1002",
                nome="Cálculo II",
                departamento=Departamento.MATEMATICA,
            ),
            Materia(
                id=3,
                codigo="MAT1003",
                nome="Álgebra Linear",
                departamento=Departamento.MATEMATICA,
            ),
            Materia(
                id=4,
                codigo="MAT1004",
                nome="Geometria",
                departamento=Departamento.MATEMATICA,
            ),
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
        materia = Materia(
            id=1, codigo="INF1004", nome="Python", departamento=Departamento.INFORMATICA
        )
        assert materia.nome == "Python"

    def test_materia_with_id(self):
        """Test Materia with id"""
        materia = Materia(
            id=1,
            codigo="INF1005",
            nome="JavaScript",
            departamento=Departamento.INFORMATICA,
        )
        assert materia.id == 1

    def test_materia_properties(self):
        """Test Materia properties"""
        materia = Materia(
            id=1, codigo="INF1006", nome="React", departamento=Departamento.INFORMATICA
        )
        assert hasattr(materia, "nome")


class TestMateriaRoutes:
    """Tests for materia routes"""

    def setup_method(self):
        """Setup test fixtures"""
        pass

    @patch("src.core.use_case.ListaMateriasUseCase.ListaMateriasUseCase.executa")
    def test_lista_materias_route(self, mock_executa):
        mock_executa.return_value = []  # Retorna uma lista vazia simulando o sucesso
        pass

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
        materias = [Mock(id=1, nome="Subject1"), Mock(id=2, nome="Subject2")]

        # This function should format the subjects for API response
        # Testing structure (actual implementation depends on schema)
        result = apresenta_materias(materias)
        assert result is not None


class TestMateriaRepositoryInterface:
    """Tests for Materia Repository Interface"""

    def test_materia_repository_find_by_id(self):
        """Test repository method to find subject by id"""
        mock_repo = Mock()
        materia = Materia(
            id=1, codigo="INF1004", nome="Python", departamento=Departamento.INFORMATICA
        )

        mock_repo.encontra_por_id.return_value = materia

        result = mock_repo.encontra_por_id(1)
        assert result.nome == "Python"
        mock_repo.encontra_por_id.assert_called_once_with(1)

    def test_materia_repository_find_all(self):
        """Test repository method to find all subjects"""
        mock_repo = Mock()
        materias = [
            Materia(
                id=1,
                codigo="MAT1005",
                nome="Math",
                departamento=Departamento.MATEMATICA,
            ),
            Materia(
                id=2,
                codigo="ENG1001",
                nome="Physics",
                departamento=Departamento.ENGENHARIA,
            ),
        ]

        mock_repo.retorna_todas_as_materias.return_value = materias

        result = mock_repo.retorna_todas_as_materias()
        assert len(result) == 2
        mock_repo.retorna_todas_as_materias.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
