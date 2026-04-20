import typer
from typing import Optional
from rich import print
from app.project_console import project_show
from app.import_project_short import project_init, project_update
from app.milestone_console import milestone_add, milestone_list, milestone_delete, milestone_status
from app.actions_console import action_add, action_list, action_delete, action_modify, action_status
from app.issues_console import issue_add, issue_list, issue_delete, issue_modify, issue_status
from app.issues_sync import sync_issues
from app.actions_sync import sync_actions
from app.works_console import work_add, work_list, work_delete, work_report, work_mark, work_sync

app = typer.Typer(add_completion=False)

@app.callback(invoke_without_command=True)
def mainii(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        print("[b magenta]PROJETA CLI[/b magenta]")
        print("Use [cyan]proj --help[/cyan] para ver os comandos disponíveis.")
        raise typer.Exit()
    
project_app = typer.Typer()
milestones_app = typer.Typer()
actions_app = typer.Typer()
issues_app = typer.Typer()
works_app = typer.Typer()

app.add_typer(project_app, name="project")
app.add_typer(milestones_app, name="milestones")
app.add_typer(actions_app, name="actions")
app.add_typer(issues_app, name="issues")
app.add_typer(works_app, name="works")


@project_app.command("init")
def typer_project_init():
    """Inicializa o projeto a partir do arquivo Project Short.md."""
    project_init()

@project_app.command("show")
def typer_project_show():
    """Mostra os detalhes do projeto atual."""
    project_show()

@project_app.command("update")
def typer_project_update():
    """Atualiza o projeto conforme o conteúdo do Project Short.md."""
    project_update()




@milestones_app.command("list")
def typer_milestone_list():
    """Lista todos os marcos do projeto."""
    milestone_list()

@milestones_app.command("add")
def typer_milestone_add(name: str):
    """Adiciona um novo marco ao projeto."""
    milestone_add(name)

@milestones_app.command("delete")
def typer_milestone_delete(id: str):
    """Exclui um marco (exige confirmação do nome tipo GitHub)."""
    milestone_delete(id)

@milestones_app.command("status")
def typer_milestone_status():
    """Altera o status de um marco interativamente."""
    milestone_status()


@actions_app.command("list")
def typer_action_list(milestone: Optional[str] = typer.Option(None, help="Filtrar por ID do marco")):
    """Lista as ações do projeto."""
    action_list(milestone)

@actions_app.command("add")
def typer_action_add(name: str, milestone: Optional[str] = typer.Option(None, help="Vincular a um marco (ID)")):
    """Adiciona uma nova ação."""
    action_add(name, milestone)

@actions_app.command("delete")
def typer_action_delete(id: str):
    """Exclui uma ação."""
    action_delete(id)

@actions_app.command("modify")
def typer_action_modify(
    id: str, 
    name: Optional[str] = typer.Option(None, help="Novo nome da ação"),
    status: Optional[str] = typer.Option(None, help="Novo status (AGUARDANDO, INICIADO, CONCLUIDO, CANCELADO)")
):
    """Modifica uma ação existente."""
    action_modify(id, name, status)

@actions_app.command("status")
def typer_action_status():
    """Altera o status de uma ação interativamente (com propagação para o marco)."""
    action_status()
    
@actions_app.command("sync")
def typer_action_sync():
    """Sincroniza as ações enviando o status do Markdown (.project/actions.md) para o sistema."""
    from app.action_md_sync import import_actions_from_markdown
    import_actions_from_markdown()

@actions_app.command("mark")
def typer_action_mark():
    """Gera/Atualiza o arquivo Markdown (.project/actions.md) com as informações do sistema."""
    from app.action_md_sync import export_actions_to_markdown
    export_actions_to_markdown()


@issues_app.command("list")
def typer_issue_list():
    """Lista as issues do projeto."""
    issue_list()

@issues_app.command("add")
def typer_issue_add(description: str):
    """Adiciona uma nova issue."""
    issue_add(description)

@issues_app.command("delete")
def typer_issue_delete(id: str):
    """Exclui uma issue."""
    issue_delete(id)

@issues_app.command("modify")
def typer_issue_modify(
    id: str, 
    description: Optional[str] = typer.Option(None, help="Nova descrição da issue"),
    status: Optional[str] = typer.Option(None, help="Novo status")
):
    """Modifica uma issue existente."""
    issue_modify(id, description, status)

@issues_app.command("sync")
def typer_issue_sync():
    """Sincroniza as issues enviando as informações do Markdown (.project/issues.md) para o sistema."""
    from app.issue_md_sync import import_issues_from_markdown
    import_issues_from_markdown()

@issues_app.command("mark")
def typer_issue_mark():
    """Gera/Atualiza o arquivo Markdown (.project/issues.md) com as informações do sistema."""
    from app.issue_md_sync import export_issues_to_markdown
    export_issues_to_markdown()

@issues_app.command("status")
def typer_issue_status():
    """Altera o status de uma issue interativamente."""
    issue_status()


@works_app.command("add")
def typer_works_add():
    """Adiciona um novo registro de trabalho (Worklog) interativamente."""
    work_add()

@works_app.command("list")
def typer_works_list():
    """Lista todos os registros de trabalho."""
    work_list()

@works_app.command("delete")
def typer_works_delete(id: str):
    """Exclui um registro de trabalho."""
    work_delete(id)

@works_app.command("report")
def typer_works_report():
    """Gera um relatório detalhado de trabalho em Markdown."""
    work_report()

@works_app.command("mark")
def typer_works_mark():
    """Gera o arquivo de sincronização de pendências .project/worklogs.md com tags do usuário."""
    work_mark()

@works_app.command("sync")
def typer_works_sync():
    """Importa as tags de trabalho do Markdown (.project/worklogs.md) para o banco de dados."""
    work_sync()



def main():
    app()

