from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

from app.project_data import ProjectData
from rich import print
from datetime import datetime, date

def select():

    data = ProjectData.load_or_create()
    data.repost_projeto()
    actions = data.list_pending_actions()

    lista_choices = []
    for action in actions:
        lista_choices.append(Choice(action.idaction, 
            name=f'{action.status.value:15} {action.sequence:3} {action.name}'))
        
    lista_choices.append(Separator())
    lista_choices.append(Choice(value=None, name="Exit"))

    idaction = inquirer.select(
            message="Select actions:",
            choices=lista_choices,
            multiselect=True,
        ).execute()[0]


    if not idaction is None:

        action = data.get_action_by_code(idaction)

        print(f'ID: {action.idaction}\nACTION: {action.name}\nSTATUS: {action.status.value}')

        description = inquirer.text(message="Enter work description:").execute()

        day = inquirer.text(message="Enter work date (YYYY-MM-DD):",
                            default=date.today().strftime("%Y-%m-%d")).execute()

        time = inquirer.text(message="Enter work time (in hours):").execute()

        data.add_works(description=description, 
                       idaction=idaction, 
                       time=float(time), 
                       work_date=day)

        response = inquirer.confirm(
            message="Save project?",
            default=True,
            confirm_letter="s",
            reject_letter="n",
            transformer=lambda result: "Yes" if result else "No",
        ).execute()

        if response:
            data.save()

if __name__ == "__main__":

    select()
