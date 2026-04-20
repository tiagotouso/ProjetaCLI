from app.project_data import ProjectData, get_db_dir
from app.models import StatusEnum
from rich import print
from rich.table import Table
from rich import box
import typer
from typing import Optional
from app.action_md_sync import sync_actions_markdown

def _check_init():
    if not (get_db_dir() / 'db.json').exists():
        print(f"[red]Erro: Projeto não inicializado. Execute [yellow]proj project init[/yellow] primeiro.[/red]")
        return False
    return True

def action_list(milestone: Optional[str] = None):
    if not _check_init(): return
    data = ProjectData.load_or_create()
    actions = data.actions
    
    if milestone:
        actions = [a for a in actions if a.idmilestone and a.idmilestone.startswith(milestone)]
    
    if not actions:
        print("[yellow]Nenhuma ação cadastrada.[/yellow]")
        return
        
    table = Table(box=box.MINIMAL, header_style="bold cyan")
    table.add_column("ID", width=10)
    table.add_column("AÇÃO", width=40)
    table.add_column("MARCO", width=30)
    table.add_column("STATUS", width=15)
    
    for a in actions:
        m_name = "-"
        if a.idmilestone:
            m = data.get_melistones_by_code(a.idmilestone)
            if m: m_name = m.name
        table.add_row(a.idaction[:8], a.name, m_name, a.status.value)
    
    print(table)

def action_add(name: str, milestone: Optional[str] = None):
    if not _check_init(): return
    data = ProjectData.load_or_create()
    
    mid = None
    if milestone:
        ms = [m for m in data.milestones if m.idmilestone.startswith(milestone)]
        if ms:
            mid = ms[0].idmilestone
            print(f"[cyan]Vinculando ao marco: {ms[0].name}[/cyan]")
        else:
            print(f"[yellow]Aviso: Marco '{milestone}' não encontrado. Criando ação sem marco.[/yellow]")
            
    data.add_actions(name, mid)
    data.save()
    sync_actions_markdown(data=data)
    print(f"[green]Ação '{name}' adicionada com sucesso![/green]")

def action_delete(id_prefix: str):
    if not _check_init(): return
    data = ProjectData.load_or_create()
    actions = [a for a in data.actions if a.idaction.startswith(id_prefix)]
    
    if not actions:
        print(f"[red]Erro: Nenhuma ação encontrada com o ID iniciando em '{id_prefix}'.[/red]")
        return
    
    if len(actions) > 1:
        print(f"[yellow]Aviso: Múltiplas ações encontradas. Seja mais específico.[/yellow]")
        return
    
    a = actions[0]
    confirm = typer.confirm(f"Tem certeza que deseja excluir a ação '{a.name}'?")
    if confirm:
        data.del_action(a.idaction)
        data.save()
        sync_actions_markdown(data=data)
        print(f"[green]Ação '{a.name}' excluída.[/green]")

def action_modify(id_prefix: str, name: Optional[str] = None, status: Optional[str] = None):
    if not _check_init(): return
    data = ProjectData.load_or_create()
    actions = [a for a in data.actions if a.idaction.startswith(id_prefix)]
    
    if not actions:
        print(f"[red]Erro: Ação não encontrada.[/red]")
        return
    
    a = actions[0]
    if name:
        a.name = name
    if status:
        status_upper = status.upper()
        found_status = None
        for s in StatusEnum:
            if s.name == status_upper:
                found_status = s
                break
        
        if found_status:
            a.status = found_status
        else:
            print(f"[red]Status inválido: {status}. Opções: {[s.name for s in StatusEnum]}[/red]")
            return
            
    if name or status:
        if status:
            data.needs_sync = True
        data.save()
        sync_actions_markdown(data=data)
        print("[green]Ação atualizada com sucesso![/green]")

def action_status():
    from InquirerPy import inquirer
    from InquirerPy.base.control import Choice
    if not _check_init(): return
        
    data = ProjectData.load_or_create()
    
    # 1. Selecionar Marco (ativos)
    milestones = [m for m in data.milestones if m.status not in [StatusEnum.CONCLUIDO, StatusEnum.CANCELADO]]
    if not milestones:
        print("[yellow]Nenhum marco ativo encontrado para atualizar ações.[/yellow]")
        return
        
    m_choice = inquirer.select(
        message="Selecione o Marco:",
        choices=[Choice(m.idmilestone, f"{m.status.value} {m.name}") for m in milestones]
    ).execute()
    
    # 2. Selecionar Ação
    actions = [a for a in data.actions if a.idmilestone == m_choice]
    if not actions:
        print("[yellow]Nenhuma ação encontrada neste marco.[/yellow]")
        return
        
    a_choice_id = inquirer.select(
        message="Selecione a Ação para alterar status:",
        choices=[Choice(a.idaction, f"{a.status.value} {a.name}") for a in actions]
    ).execute()
    
    action = data.get_action_by_code(a_choice_id)
    
    # 3. Novo Status
    new_status = inquirer.select(
        message=f"Novo Status para '{action.name}':",
        choices=[Choice(s, s.value) for s in StatusEnum]
    ).execute()
    
    action.status = new_status
    data.needs_sync = True
    data.save()
    sync_actions_markdown(data=data)
    print(f"[green]Status da ação atualizado para {action.status.value}[/green]")
