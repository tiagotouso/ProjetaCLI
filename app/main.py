import typer
from rich import print
from app.project_console import project_show

app = typer.Typer(add_completion=False)

@app.callback(invoke_without_command=True)
def mainii(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        print("[red] Bem-vindo ao ProjetaCLI! [/red]")
        typer.echo(ctx.get_help())  # Mostra o help programaticamente
        raise typer.Exit()
    
project_app = typer.Typer()
actions_app = typer.Typer()
issues_app = typer.Typer()
works_app = typer.Typer()

app.add_typer(project_app, name="project")
app.add_typer(actions_app, name="actions")
app.add_typer(issues_app, name="issues")
app.add_typer(works_app, name="works")


@project_app.command("show")
def typer_project_show():
    project_show()


@works_app.command("show")
def typer_works_show():
    print("Showing works")



def main():
    app()

