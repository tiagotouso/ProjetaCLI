from app.project_data import ProjectData, get_db_dir
from rich import print
from rich.table import Table
from rich import box
import typer

def milestone_list():
    from pathlib import Path
    if not (get_db_dir() / 'db.json').exists():
        print("[red]Erro: Projeto não inicializado. Execute [yellow]proj project init[/yellow] primeiro.[/red]")
        return
    from app.models import StatusEnum
    data = ProjectData.load_or_create()
    if not data.milestones:
        print("[yellow]Nenhum marco cadastrado.[/yellow]")
        return
    
    table = Table(box=box.MINIMAL, header_style="bold cyan")
    table.add_column("ID", width=10)
    table.add_column("MARCO", width=35)
    table.add_column("STATUS", width=15)
    table.add_column("AG.", justify="center", style="yellow")
    table.add_column("INI.", justify="center", style="blue")
    table.add_column("CONC.", justify="center", style="green")
    table.add_column("CANC.", justify="center", style="red")
    table.add_column("% CONC.", justify="right", style="bold green")
    
    for m in data.milestones:
        m_actions = [a for a in data.actions if a.idmilestone == m.idmilestone]
        
        c_ag = sum(1 for a in m_actions if a.status == StatusEnum.AGUARDANDO)
        c_ini = sum(1 for a in m_actions if a.status == StatusEnum.INICIADO)
        c_conc = sum(1 for a in m_actions if a.status == StatusEnum.CONCLUIDO)
        c_canc = sum(1 for a in m_actions if a.status == StatusEnum.CANCELADO)
        
        total = len(m_actions)
        p_conc = (c_conc / total * 100) if total > 0 else 0
            
        table.add_row(
            m.idmilestone[:8], 
            m.name, 
            m.status.value,
            str(c_ag),
            str(c_ini),
            str(c_conc),
            str(c_canc),
            f"{p_conc:.0f}%"
        )
    
    print(table)

    total_actions = len(data.actions)
    total_conc = sum(1 for a in data.actions if a.status == StatusEnum.CONCLUIDO)
    total_p = (total_conc / total_actions * 100) if total_actions > 0 else 0
    
    print(f"\n[bold cyan]PROGRESSO TOTAL DO PROJETO: {total_p:.1f}%[/bold cyan]")
    print("-" * 30)

def milestone_add(name: str):
    from pathlib import Path
    if not (Path('.project') / 'db.json').exists():
        print("[red]Erro: Projeto não inicializado. Execute [yellow]proj project init[/yellow] primeiro.[/red]")
        return
    data = ProjectData.load_or_create()
    idm = data.add_milestones(name)
    data.save()
    print(f"[green]Marco '{name}' adicionado com sucesso! (ID: {idm[:8]})[/green]")

def milestone_delete(id_prefix: str):
    from pathlib import Path
    if not (Path('.project') / 'db.json').exists():
        print("[red]Erro: Projeto não inicializado. Execute [yellow]proj project init[/yellow] primeiro.[/red]")
        return
    data = ProjectData.load_or_create()
    # Encontrar milestone pelo prefixo do ID
    milestones = [m for m in data.milestones if m.idmilestone.startswith(id_prefix)]
    
    if not milestones:
        print(f"[red]Erro: Nenhum marco encontrado com o ID iniciando em '{id_prefix}'.[/red]")
        return
    
    if len(milestones) > 1:
        print(f"[yellow]Aviso: Múltiplos marcos encontrados ({len(milestones)}). Por favor, forneça um ID mais específico.[/yellow]")
        return
    
    m = milestones[0]
    print(f"[bold red]ATENÇÃO:[/bold red] Você está prestes a excluir o marco [bold]'{m.name}'[/bold].")
    print(f"Isso desvinculará todas as ações associadas a este marco.")
    
    confirm = typer.prompt(f"Para confirmar a exclusão, digite o nome do marco exatamente como aparece acima")
    
    if confirm == m.name:
        data.del_milestone(m.idmilestone)
        data.save()
        print(f"[green]Marco '{m.name}' excluído com sucesso![/green]")
    else:
        print("[red]Confirmação falhou. O nome digitado não coincide. Operação cancelada.[/red]")

def milestone_status():
    from InquirerPy import inquirer
    from InquirerPy.base.control import Choice
    from pathlib import Path
    from app.models import StatusEnum
    
    if not (Path('.project') / 'db.json').exists():
        print("[red]Erro: Projeto não inicializado. Execute [yellow]proj project init[/yellow] primeiro.[/red]")
        return
        
    data = ProjectData.load_or_create()
    
    if not data.milestones:
        print("[yellow]Nenhum marco encontrado.[/yellow]")
        return
        
    m_choice_id = inquirer.select(
        message="Selecione o Marco para alterar status:",
        choices=[Choice(m.idmilestone, f"{m.status.value} {m.name}") for m in data.milestones]
    ).execute()
    
    m_obj = data.get_melistones_by_code(m_choice_id)
    
    new_status = inquirer.select(
        message=f"Novo status para '{m_obj.name}':",
        choices=[Choice(s, s.value) for s in StatusEnum],
        default=m_obj.status
    ).execute()
    
    m_obj.status = new_status
    data.save()
    print(f"[green]Status de '{m_obj.name}' atualizado para {m_obj.status.value}[/green]")
