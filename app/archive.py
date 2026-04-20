from pathlib import Path
from app.project_data import ProjectData, get_db_dir

def write_pydantic(modelo: ProjectData, caminho_arquivo=None) -> None:
    db_dir = get_db_dir()
    if caminho_arquivo is None:
        caminho_arquivo = db_dir / 'db.json'
    
    db_dir.mkdir(parents=True, exist_ok=True)
    json_string = modelo.model_dump_json(indent=4)
    Path(caminho_arquivo).write_text(json_string, encoding='utf-8')

def read_pydantic(caminho_arquivo=None) -> ProjectData:
    if caminho_arquivo is None:
        caminho_arquivo = get_db_dir() / 'db.json'
    
    json_string = Path(caminho_arquivo).read_text(encoding='utf-8')
    modelo_carregado = ProjectData.model_validate_json(json_string)
    return modelo_carregado


