from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator


from app.project_data import ProjectData
from rich import print
from datetime import datetime, date
from app.models import StatusEnum
from app.archive import read_pydantic, write_pydantic


def update_action_status():

    data = ProjectData.load_or_create()

    actions = data.list_pending_actions()
    
    if not actions:
        print("[green]Todas as ações estão concluídas.[/green]")
        return

    choices = [Choice(action.idaction, name=f"{action.status.value:15} {action.sequence:3} {action.name}") for action in actions]
    choices.append(Separator())
    choices.append(Choice(value=None, name="Sair"))

    idaction = inquirer.select(
        message="Selecione uma ação para atualizar o status:",
        choices=choices
    ).execute()

    if not idaction:
        print("[yellow]Operação cancelada.[/yellow]")
        return

    action = data.get_action_by_code(idaction)
    print(f"Ação selecionada: [bold]{action.name}[/bold] (Status atual: {action.status.value})")

    status_choices = [Choice(status, name=status.value) for status in StatusEnum]
    new_status = inquirer.select(
        message="Selecione o novo status:",
        choices=status_choices
    ).execute()

    action.status = new_status
    print(f"[cyan]Ação '{action.name}' atualizada para o status '{new_status.value}'.[/cyan]")

    confirm = inquirer.confirm(
        message="Deseja salvar o projeto?",
        default=True,
        confirm_letter="s",
        reject_letter="n",
        transformer=lambda result: "Sim" if result else "Não",
    ).execute()

    if confirm:
        data.save()
        print("[green]Projeto salvo com sucesso![/green]")
    else:
        print("[yellow]Alteração não salva.[/yellow]")

if __name__ == "__main__":
    update_action_status()
