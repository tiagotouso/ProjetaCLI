
from pathlib import Path
from app.project_data import ProjectData

path_db = Path('.project') / 'db.json'

def write_pydantic(modelo: ProjectData, caminho_arquivo=path_db) -> None:

    path_dir = Path('.project')
    path_dir.mkdir(parents=True, exist_ok=True)

    json_string = modelo.model_dump_json(indent=4)
    Path(caminho_arquivo).write_text(json_string, encoding='utf-8')


def read_pydantic(caminho_arquivo: Path | str = path_db) -> ProjectData:

    json_string = Path(caminho_arquivo).read_text(encoding='utf-8')
    modelo_carregado = ProjectData.model_validate_json(json_string)

    return modelo_carregado

