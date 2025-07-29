from app.archive import read_pydantic
from app.project_data import ProjectData
from pathlib import Path
from rich import print


path_db = Path('.project') / 'db.json'

if __name__ == '__main__':
    
    data = read_pydantic()
    project = data.project
    print(project.name)
    print(project.description)
    print()

    actions = data.actions
    for action in actions:
        milestone_name = ''
        if action.cdmilestone != None:
            milestone = data.get_melistones_by_code(action.cdmilestone)
            if milestone != None:
                milestone_name = milestone.name
        print(f'{action.cdaction:4} {action.name:50} {milestone_name:30} {action.status.value}')

    print()
    issues = data.issues
    for issue in issues:
        print(f'{issue.cdissues} - {issue.description}')



