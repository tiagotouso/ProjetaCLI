import re
from pathlib import Path
from app.project_data import ProjectData, get_db_dir
from app.models import Action, StatusEnum
from rich import print

def get_actions_md_path() -> Path:
    return get_db_dir() / 'actions.md'

def import_actions_from_markdown():
    """Importa o status das ações do arquivo Markdown para o banco de dados."""
    if not (get_db_dir() / 'db.json').exists():
        return
        
    data = ProjectData.load_or_create()
    ACTIONS_MD = get_actions_md_path()
    
    if not ACTIONS_MD.exists():
        print(f"[yellow]Aviso: Arquivo {ACTIONS_MD} não encontrado para importação.[/yellow]")
        return

    # 1. Ler do MD
    txt = ACTIONS_MD.read_text(encoding='utf-8')
    pattern = r"- \[(x| )\] (.*?) <!-- \[id:(.*?)\] -->"
    matches = re.finditer(pattern, txt)
    
    md_updates = {}
    for m in matches:
        is_done = m.group(1).lower() == 'x'
        action_id = m.group(3)
        md_updates[action_id] = StatusEnum.CONCLUIDO if is_done else StatusEnum.AGUARDANDO

    # 2. Atualizar Sistema
    mudou = False
    for a in data.actions:
        if a.idaction in md_updates:
            novo_status = md_updates[a.idaction]
            if a.status != novo_status:
                a.status = novo_status
                mudou = True
                data.needs_sync = True
    
    if mudou:
        data.save()
        print("[green]Status das ações importados do Markdown para o sistema.[/green]")
    else:
        print("[blue]Nenhuma alteração detectada no Markdown de ações.[/blue]")

def export_actions_to_markdown():
    """Gera o arquivo Markdown (.project/actions.md) a partir dos dados do sistema."""
    if not (get_db_dir() / 'db.json').exists():
        return
        
    data = ProjectData.load_or_create()
    ACTIONS_MD = get_actions_md_path()
    
    _export_actions_to_md(data, ACTIONS_MD)
    print(f"[green]Arquivo {ACTIONS_MD} atualizado com os marcos e ações do sistema.[/green]")

def sync_actions_markdown(import_data=True, data=None):
    if import_data:
        import_actions_from_markdown()
    else:
        export_actions_to_markdown()

def _export_actions_to_md(data, path):
    lines = ["# Ações do Projeto\n"]
    
    # Agrupar por Milestone
    by_milestone = {}
    for a in data.actions:
        m_id = a.idmilestone or "none"
        by_milestone.setdefault(m_id, []).append(a)
    
    # Ordenar milestones pela sequência original se possível
    sorted_m_ids = []
    milestone_names = {"none": "Outras Ações (Sem Marco)"}
    
    for m in sorted(data.milestones, key=lambda x: x.sequence):
        sorted_m_ids.append(m.idmilestone)
        milestone_names[m.idmilestone] = m.name
        
    if "none" in by_milestone:
        sorted_m_ids.append("none")

    for m_id in sorted_m_ids:
        if m_id not in by_milestone: continue
        
        lines.append(f"\n## 🚩 {milestone_names[m_id]}")
        for a in sorted(by_milestone[m_id], key=lambda x: x.sequence):
            check = "x" if a.status == StatusEnum.CONCLUIDO else " "
            lines.append(f"- [{check}] {a.name} <!-- [id:{a.idaction}] -->")
            
    path.write_text("\n".join(lines) + "\n", encoding='utf-8')
    # print(f"[yellow]Arquivo de ações atualizado: {path}[/yellow]")
