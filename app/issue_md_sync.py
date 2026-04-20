import re
from pathlib import Path
from app.project_data import ProjectData, get_db_dir
from app.models import Issues, StatusEnum
from app.uuid_utils import generate_uuid
from rich import print
from datetime import date

ISSUES_MD = get_db_dir() / 'issues.md'

def import_issues_from_markdown():
    """Importa o status e descrições das issues do arquivo Markdown para o banco de dados."""
    if not (get_db_dir() / 'db.json').exists():
        return
        
    data = ProjectData.load_or_create()
    
    if not ISSUES_MD.exists():
        print(f"[yellow]Aviso: Arquivo {ISSUES_MD} não encontrado para importação.[/yellow]")
        return

    # 1. Ler do MD
    md_issues = []
    txt = ISSUES_MD.read_text(encoding='utf-8')
    pattern = r"[-*]\s*\[([ xX])\]\s+(.*?)(?:\s+<!--\s*\[id:(.*?)\]\s*-->)?$"
    
    for line in txt.split('\n'):
        line = line.strip()
        if not line: continue
        match = re.match(pattern, line)
        if match:
            check = match.group(1)
            desc = match.group(2).strip()
            id_val = match.group(3)
            status = StatusEnum.CONCLUIDO if check.lower() == 'x' else StatusEnum.AGUARDANDO
            md_issues.append({'idissues': id_val, 'description': desc, 'status': status})

    # 2. Atualizar Sistema
    sys_ids = {i.idissues: i for i in data.issues}
    today = date.today().isoformat()
    mudou = False

    for mi in md_issues:
        if mi['idissues'] and mi['idissues'] in sys_ids:
            sys_issue = sys_ids[mi['idissues']]
            if sys_issue.description != mi['description'] or sys_issue.status != mi['status']:
                sys_issue.description = mi['description']
                sys_issue.status = mi['status']
                mudou = True
        elif not mi['idissues']:
            data.add_issues(mi['description'], today)
            data.issues[-1].status = mi['status']
            mudou = True
    
    if mudou:
        data.save()
        print(f"[green]Dados importados do Markdown para o sistema ({len(data.issues)} issues).[/green]")
    else:
        print("[blue]Nenhuma alteração detectada no Markdown de issues.[/blue]")

def export_issues_to_markdown():
    """Gera o arquivo Markdown (.project/issues.md) a partir dos dados atuais do sistema."""
    if not (get_db_dir() / 'db.json').exists():
        return
        
    data = ProjectData.load_or_create()
    
    db_dir = get_db_dir()
    db_dir.mkdir(exist_ok=True, parents=True)

    lines = ["# Issues do Projeto\n"]
    if not data.issues:
        lines.append("\n*Nenhuma issue cadastrada.*")
    else:
        for i in data.issues:
            check = "x" if i.status == StatusEnum.CONCLUIDO else " "
            lines.append(f"- [{check}] {i.description} <!-- [id:{i.idissues}] -->")
    
    ISSUES_MD.write_text("\n".join(lines) + "\n", encoding='utf-8')
    print(f"[green]Arquivo {ISSUES_MD} atualizado com dados do sistema.[/green]")

def sync_issues_markdown(import_data=True, data=None):
    if import_data:
        import_issues_from_markdown()
    else:
        export_issues_to_markdown()
