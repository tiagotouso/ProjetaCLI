from app.project_data import ProjectData
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.text import Text

from app.action_actions import update_action_status


console = Console()

def print_main_menu():
	table = Table.grid(padding=(0,2))
	table.add_column(justify="center", style="bold cyan")
	table.add_row("[b magenta]PROJETA CLI[/b magenta]")
	table.add_row("")
	table.add_row("[bold]Project[/bold]   [bold]Milestones[/bold]   [bold]Actions[/bold]   [bold]Issues[/bold]   [bold]Works[/bold]")
	panel = Panel(Align.center(table), title="[b green]Menu Principal[/b green]", border_style="bright_blue")
	console.clear()
	console.print(panel)

def print_submenu(title, options):
	table = Table.grid(padding=(0,2))
	table.add_column(justify="center", style="bold yellow")
	table.add_row(f"[b cyan]{title}[/b cyan]")
	table.add_row("")
	for opt in options:
		table.add_row(f"[white]{opt.capitalize()}[/white]")
	panel = Panel(Align.center(table), title=f"[b green]{title}[/b green]", border_style="bright_magenta")
	console.clear()
	console.print(panel)


def submenu(title, options):
	
	while True:
		print_submenu(title, options)
		choices = [Choice(opt, name=opt.capitalize()) for opt in options]
		choices.append(Separator())
		choices.append(Choice("voltar", name="Voltar"))
		result = inquirer.select(
			message=f"{title}: Selecione uma opção:",
			choices=choices
		).execute()
		console.print(f"[bold green]Você selecionou:[/bold green] [yellow]{result}[/yellow]")
		if result == "voltar":
			break
		if title.lower() == "project":
			if result.lower() == "report":
				project = ProjectData.load_or_create()
				project.report_projeto()
				console.print("[bold cyan]Relatório do projeto gerado com sucesso![/bold cyan]")
		elif title.lower() == "milestones":
			...
		elif title.lower() == "actions":

			if result.lower() == "status":
				update_action_status()
			
		elif title.lower() == "issues":
			...
		elif title.lower() == "works":
			...
			# inquirer.message(
			# 	message="Relatório do projeto salvo em 'Project Report.md'! Pressione Enter para continuar."
			# ).execute()
		# Aqui você pode adicionar outras ações para cada opção
		# else:
		#     ...

def main_menu():
	
	main_choices = [
		Choice("project", name="📁 Project"),
		Choice("milestones", name="🚩 Milestones"),
		Choice("actions", name="⚡️ Actions"),
		Choice("issues", name="🐛 Issues"),
		Choice("works", name="⏱️  Works"),
		Separator(),
		Choice("exit", name="❌ Exit")
	]

	while True:
		print_main_menu()
		selected = inquirer.select(
			message="Menu principal: Selecione uma categoria:",
			choices=main_choices
		).execute()

		if selected == "exit":
			console.print("[bold red]Saindo...[/bold red]")
			break
		elif selected == "project":
			submenu("Project", ["show", "edit", "report"])
		elif selected == "milestones":
			submenu("Milestones", ["show", "add", "edit", "delete"])
		elif selected == "actions":
			submenu("Actions", ["show", "status", "add", "edit", "delete"])
		elif selected == "issues":
			submenu("Issues", ["show", "add", "edit", "delete"])
		elif selected == "works":
			submenu("Works", ["show", "add", "edit", "delete"])

if __name__ == "__main__":
	
	main_menu()
	
