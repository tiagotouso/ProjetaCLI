from app.archive import read_pydantic
from app.project_data import ProjectData
from pathlib import Path
from rich import print


path_db = Path('.project') / 'db.json'

def project_show():

    if not path_db.exists():
        print("[red]Erro: Projeto não inicializado.[/red]")
        print("Certifique-se de que o arquivo [bold]Project Short.md[/bold] existe e rode a importação:")
        print("[yellow]python app/import_project_short.py[/yellow]")
        return

    data = read_pydantic()
    from app.sync_manager import run_sync_tasks
    run_sync_tasks(data)
    project = data.project
    print('-' * 20)
    print(project.name)
    print()
    print(project.description)
    print()

    from rich.table import Table
    from rich.console import Console
    from rich import box
    console = Console()

    table = Table(show_header=True, header_style="bold cyan", box=box.MINIMAL)
    table.add_column("ID", width=10)
    table.add_column("AÇÃO", width=50)
    table.add_column("MARCO", width=30)
    table.add_column("STATUS", width=15)

    actions = data.actions
    for action in actions:
        milestone_name = '-'
        if action.idmilestone != None:
            milestone = data.get_melistones_by_code(action.idmilestone)
            if milestone:
                milestone_name = milestone.name
        
        table.add_row(
            action.idaction[:8],
            action.name,
            milestone_name,
            action.status.value
        )
    
    try:
        console.print(table)

        if data.issues:
            print("\n[bold yellow]🐛 Issues[/bold yellow]")
            issues_table = Table(show_header=True, header_style="bold yellow", box=box.MINIMAL)
            issues_table.add_column("ID", width=10)
            issues_table.add_column("DESCRIÇÃO")
            issues_table.add_column("STATUS")
            
            for issue in data.issues:
                issues_table.add_row(issue.idissues[:8], issue.description, issue.status.value)
            console.print(issues_table)
    except UnicodeEncodeError:
        print("\n[yellow]Aviso: Não foi possível exibir alguns caracteres especiais (emojis) neste terminal.[/yellow]")
        print("O arquivo [bold]Project Report.md[/bold] foi atualizado corretamente.")


if __name__ == '__main__':
    
    project_show()


def project_sync():
    """Sincroniza o status das ações, issues e tags de trabalho a partir dos arquivos Markdown."""
    from app.action_md_sync import sync_actions_markdown
    from app.issue_md_sync import sync_issues_markdown
    from app.works_console import work_sync
    
    try:
        print("[bold cyan]🔄 Iniciando sincronização global do projeto...[/bold cyan]")
        
        # Sincroniza Ações
        sync_actions_markdown()
        
        # Sincroniza Issues
        sync_issues_markdown()

        # Sincroniza Trabalhos (Log de horas)
        work_sync()
        
        print("\n[bold green]✅ Projeto sincronizado com sucesso![/bold green]")
    except UnicodeEncodeError:
        print("\n[yellow]Aviso: Não foi possível exibir alguns caracteres especiais (emojis) neste terminal.[/yellow]")
        print("[green]A sincronização foi concluída com sucesso, mas alguns ícones não puderam ser exibidos.[/green]")
