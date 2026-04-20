from app.project_data import ProjectData, get_db_dir
from app.models import StatusEnum
from rich import print
from rich.table import Table
from rich import box
import typer
from typing import Optional
from datetime import date
from pathlib import Path
from app.issue_md_sync import sync_issues_markdown

def _check_init():
    if not (get_db_dir() / 'db.json').exists():
        print(f"[red]Erro: Projeto não inicializado. Execute [yellow]proj project init[/yellow] primeiro.[/red]")
        return False
    return True

def issue_list():
    if not _check_init(): return
    data = ProjectData.load_or_create()
    if not data.issues:
        print("[yellow]Nenhuma issue encontrada.[/yellow]")
        return
    
    table = Table(box=box.MINIMAL, header_style="bold yellow")
    table.add_column("ID", width=10)
    table.add_column("DESCRIÇÃO", width=50)
    table.add_column("DATA", width=12)
    table.add_column("STATUS", width=15)
    
    for i in data.issues:
        table.add_row(i.idissues[:8], i.description, i.date, i.status.value)
    
    print(table)

def issue_add(description: str):
    if not _check_init(): return
    data = ProjectData.load_or_create()
    today = date.today().isoformat()
    data.add_issues(description, today)
    data.save()
    sync_issues_markdown()
    print(f"[green]Issue adicionada com sucesso![/green]")

def issue_delete(id_prefix: str):
    if not _check_init(): return
    data = ProjectData.load_or_create()
    issues = [i for i in data.issues if i.idissues.startswith(id_prefix)]
    
    if not issues:
        print(f"[red]Erro: Nenhuma issue encontrada com o ID iniciando em '{id_prefix}'.[/red]")
        return
    
    if len(issues) > 1:
        print(f"[yellow]Aviso: Múltiplas issues encontradas. Seja mais específico.[/yellow]")
        return
    
    i = issues[0]
    confirm = typer.confirm(f"Tem certeza que deseja excluir a issue '{i.description[:30]}...'?")
    if confirm:
        data.del_issue(i.idissues)
        data.save()
        sync_issues_markdown()
        print(f"[green]Issue excluída.[/green]")

def issue_modify(id_prefix: str, description: Optional[str] = None, status: Optional[str] = None):
    if not _check_init(): return
    data = ProjectData.load_or_create()
    issues = [i for i in data.issues if i.idissues.startswith(id_prefix)]
    
    if not issues:
        print(f"[red]Erro: Issue não encontrada.[/red]")
        return
    
    i = issues[0]
    if description:
        i.description = description
    if status:
        status_upper = status.upper()
        found_status = None
        for s in StatusEnum:
            if s.name == status_upper:
                found_status = s
                break
        
        if found_status:
            i.status = found_status
        else:
            print(f"[red]Status inválido: {status}. Opções: {[s.name for s in StatusEnum]}[/red]")
            return
            
    if description or status:
        data.needs_sync = True
        data.save()
        sync_issues_markdown()
        print("[green]Issue atualizada com sucesso![/green]")

def issue_status():
    from InquirerPy import inquirer
    from InquirerPy.base.control import Choice
    
    if not _check_init(): return
    data = ProjectData.load_or_create()
    
    if not data.issues:
        print("[yellow]Nenhuma issue encontrada.[/yellow]")
        return
        
    i_choice_id = inquirer.select(
        message="Selecione a Issue para alterar status:",
        choices=[Choice(i.idissues, f"{i.status.value} {i.description[:50]}") for i in data.issues]
    ).execute()
    
    i_obj = data.get_issue_by_code(i_choice_id)
    
    new_status = inquirer.select(
        message=f"Novo status para a issue:",
        choices=[Choice(s, s.value) for s in StatusEnum],
        default=i_obj.status
    ).execute()
    
    i_obj.status = new_status
    data.needs_sync = True
    data.save()
    sync_issues_markdown()
    print(f"[green]Status da issue atualizado para {i_obj.status.value}[/green]")
