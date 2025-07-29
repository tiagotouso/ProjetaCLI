from app.metadados import Project, Milestones, Action, Issues, WorkLog, StatusEnum
from typing import List, Optional
from pydantic import BaseModel, Field
from rich import print
from pathlib import Path

class ProjectData(BaseModel):
    project: Project
    milestones: List[Milestones] = Field(default_factory=list)
    actions: List[Action] = Field(default_factory=list)
    issues: List[Issues] = Field(default_factory=list)
    works: List[WorkLog] = Field(default_factory=list)

    @classmethod
    def load_or_create(cls, code: Optional[str] = None, name: Optional[str] = None, description: Optional[str] = None) -> 'ProjectData':
        """
        Método de fábrica que carrega um projeto de 'db.json' se existir,
        ou cria um novo projeto caso contrário.
        """
        path_db = Path('.project') / 'db.json'
        
        if path_db.exists():
            # Se o arquivo existe, ele é lido e validado.
            # model_validate_json já retorna uma instância completa da classe ProjectData.
            json_data = path_db.read_text(encoding='utf-8')
            return cls.model_validate_json(json_data)
        else:
            # Se o arquivo não existe, um novo projeto é criado.
            # Verifica se os argumentos necessários para a criação foram fornecidos.
            if not all([code, name, description]):
                raise ValueError("Para criar um novo projeto, os argumentos 'code', 'name' e 'description' são obrigatórios.")
            
            # Cria o objeto Project interno
            project_info = Project(
                cdproject=code.strip(),
                name=name.strip(),
                description=description.strip(),
                status=StatusEnum.AGUARDANDO
            )
            # Retorna uma nova instância da classe, passando o objeto Project recém-criado.
            # As listas (milestones, actions, etc.) serão inicializadas como vazias pelo default_factory.
            return cls(project=project_info)

    def add_milestones(self, name: str) -> str:
        '''Adiciona um novo marco ao projeto.'''
        code = len(self.milestones) + 1
        milestones = Milestones(
            cdmilestone=str(code),
            name=name.strip(),
            status=StatusEnum.AGUARDANDO
        )
        self.milestones.append(milestones)

    def add_actions(self, name: str, cdgrupo: Optional[str] = None):
        '''Adiciona uma nova ação ao projeto, opcionalmente vinculada a um grupo.'''
        code = str(len(self.actions) + 1)
        action = Action(
            cdgroup=cdgrupo,
            cdaction=code,
            name=name.strip(),
            status=StatusEnum.AGUARDANDO
        )
        self.actions.append(action)

    def add_issues(self, description: str, date: str, status: StatusEnum = StatusEnum.AGUARDANDO):
        '''Adiciona uma nova issue (problema/tarefa) ao projeto.'''
        code = str(len(self.issues) + 1)
        issue = Issues(
            cdissues=code,
            description=description,
            status=status,
            date=date
        )
        self.issues.append(issue)

    def add_works(self, description: str, time: str, work_date: str):
        '''Adiciona um novo apontamento de trabalho (horas) ao projeto.'''
        code = str(len(self.works) + 1)
        novo_work = WorkLog(
            code=code,
            description=description,
            time=time,
            date=work_date
        )
        self.works.append(novo_work)

    def get_melistones_by_code(self, cdmilestone: str) -> Optional[Milestones]:
        return next((milestone for milestone in self.milestones if milestone.cdmilestone == cdmilestone), None)
    
    def get_issue_by_code(self, cdissues: str) -> Optional[Issues]:
        return next((issue for issue in self.issues if issue.cdissues == cdissues), None)

    def repost_projeto(self):
        # Imprime o objeto de dados completo para verificação
        report = f'# 🎯 {self.project.name}\n\n> {self.project.description}\n'

        milestonetxt = ''
        if len(self.actions) > 0:
            report += '\n## ⚡️ Actions\n\n'
            for action in self.actions:
                if action.cdmilestone is not None:
                    milestone = self.get_melistones_by_code(action.cdmilestone)
                    if milestone and milestonetxt != milestone.name:
                        milestonetxt = milestone.name
                        report += f'\n### 🚩 {milestonetxt}\n'
                
                report += f'- [ ] {action.name} {action.status.value}\n'

        if len(self.issues) > 0:
            report += '\n## ⚠️ Issues\n\n'
            for issue in self.issues:
                report += f'- {issue.description} {issue.status.value} - {issue.date}\n'

        with open('Project Report.md', 'w', encoding='utf-8') as f:
            f.write(report)


if __name__ == '__main__':

    # data = ProjectData.load_or_create()
    # data.repost_projeto()
    # print(data)

    data = ProjectData.load_or_create('1', 'projeto1', 'descrição do projeto')
    data.repost_projeto()
    print(data)