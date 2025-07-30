from app.archive import read_pydantic
from app.project_data import ProjectData
from pathlib import Path
from rich import print


path_db = Path('.project') / 'db.json'

def project_show():

    data = read_pydantic()
    project = data.project
    print('-' * 20)
    print(project.name)
    print()
    print(project.description)
    print()

    actions = data.actions
    for action in actions:
        milestone_name = ''
        if action.cdmilestone != None:
            milestone = data.get_melistones_by_code(action.cdmilestone)
            milestone_name = milestone.name
        
        action_txt = action.name
        if len(action_txt) > 50:
            action_txt = action_txt[:46] + '...'

        if len(milestone_name) > 50:
            milestone_name = milestone_name[:26] + '...'

        print(f'{action.cdaction:4} {action_txt:50} {milestone_name:30} {action.status.value}')

    print()
    issues = data.issues
    for issue in issues:
        print(f'{issue.cdissues} - {issue.description}')


if __name__ == '__main__':
    
    project_show()

