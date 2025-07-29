
import pytest
import json
from pathlib import Path
from unittest.mock import MagicMock

from app.archive import write_pydantic, read_pydantic
from app.project_data import ProjectData
from app.metadados import Project, StatusEnum

@pytest.fixture
def sample_project_data():
    """Cria um objeto ProjectData de exemplo para ser usado nos testes."""
    project = Project(
        cdproject="PROJ-TEST-123",
        name="Test Project for Archive",
        description="A sample project to test read/write functions.",
        status=StatusEnum.INICIADO
    )
    return ProjectData(project=project, milestones=[], actions=[], issues=[], worklog=[])

@pytest.fixture
def mock_path(monkeypatch): 
    """Mock para o objeto Path para evitar interações com o sistema de arquivos."""
    mock = MagicMock(spec=Path)
    monkeypatch.setattr("app.archive.Path", mock)
    return mock


class TestWritePydantic:
    def test_write_pydantic_calls_model_dump(self, sample_project_data, mock_path, monkeypatch):
        """Verifica se a função de escrita chama a serialização do modelo."""
        mock_dump = MagicMock(return_value="{}")
        monkeypatch.setattr("app.project_data.ProjectData.model_dump_json", mock_dump)
        write_pydantic(sample_project_data)
        mock_dump.assert_called_once_with(indent=4)

    def test_write_pydantic_calls_write_text(self, sample_project_data, mock_path):
        """Verifica se a função de escrita chama o método de escrita de arquivo."""
        json_string = sample_project_data.model_dump_json(indent=4)
        # Instancia o mock para o caminho do arquivo específico
        mock_file_path = mock_path.return_value
        write_pydantic(sample_project_data)
        mock_file_path.write_text.assert_called_once_with(json_string, encoding='utf-8')


class TestReadPydantic:
    def test_read_pydantic_calls_read_text(self, mock_path):
        """Verifica se a função de leitura chama o método de leitura de arquivo."""
        mock_file_path = mock_path.return_value
        mock_file_path.read_text.return_value = ProjectData(project=Project(cdproject='a', name='b', description='c', status=StatusEnum.AGUARDANDO), milestones=[], actions=[], issues=[], worklog=[]).model_dump_json()
        read_pydantic()
        mock_file_path.read_text.assert_called_once_with(encoding='utf-8')

    def test_read_pydantic_returns_project_data_instance(self, sample_project_data, mock_path):
        """Verifica se a função de leitura retorna uma instância de ProjectData."""
        json_string = sample_project_data.model_dump_json()
        mock_file_path = mock_path.return_value
        mock_file_path.read_text.return_value = json_string
        
        loaded_model = read_pydantic()
        
        assert isinstance(loaded_model, ProjectData)

    def test_read_pydantic_data_is_correct(self, sample_project_data, mock_path):
        """Verifica se os dados carregados pela função de leitura estão corretos."""
        json_string = sample_project_data.model_dump_json()
        mock_file_path = mock_path.return_value
        mock_file_path.read_text.return_value = json_string

        loaded_model = read_pydantic()

        assert loaded_model == sample_project_data
