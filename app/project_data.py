from app.models import Project, Milestones, Action, Issues, WorkLog, StatusEnum
from app.uuid_utils import generate_uuid
from typing import List, Optional
from pydantic import BaseModel, Field
from rich import print
from pathlib import Path
import os

def get_db_dir() -> Path:
    """Retorna o diretório do banco de dados (padrão: .project)."""
    dir_name = os.getenv("PROJ_DB_DIR", ".project")
    return Path(dir_name)

class ProjectData(BaseModel):
    project: Project
    milestones: List[Milestones] = Field(default_factory=list)
    actions: List[Action] = Field(default_factory=list)
    issues: List[Issues] = Field(default_factory=list)
    works: List[WorkLog] = Field(default_factory=list)
    needs_sync: bool = False

    @classmethod
    def load_or_create(cls, name: Optional[str] = None, description: Optional[str] = None) -> 'ProjectData':
        """
        Método de fábrica que carrega um projeto de 'db.json' se existir,
        ou cria um novo projeto caso contrário.
        """
        path_db = get_db_dir() / 'db.json'
        
        if path_db.exists():
            json_data = path_db.read_text(encoding='utf-8')
            return cls.model_validate_json(json_data)
        else:
            if not all([name, description]):
                raise FileNotFoundError("Projeto não inicializado. Execute 'proj project init' primeiro.")
            
            project_info = Project(
                idproject=generate_uuid(),
                name=name.strip(),
                description=description.strip(),
                status=StatusEnum.AGUARDANDO
            )
            return cls(project=project_info)

    def add_milestones(self, name: str) -> str:
        self.needs_sync = True
        idmilestone=generate_uuid()
        milestones = Milestones(
            idmilestone=idmilestone,
            name=name.strip(),
            status=StatusEnum.AGUARDANDO,
            sequence=len(self.milestones) + 1
        )
        self.milestones.append(milestones)
        return idmilestone

    def add_actions(self, name: str, idmilestone: Optional[str] = None):
        self.needs_sync = True
        action = Action(
            idmilestone=idmilestone,
            idaction=generate_uuid(),
            name=name.strip(),
            status=StatusEnum.AGUARDANDO,
            sequence=len(self.actions) + 1
        )
        self.actions.append(action)

    def add_issues(self, description: str, date: str):
        self.needs_sync = True
        issue = Issues(
            idissues=generate_uuid(),
            description=description,
            status=StatusEnum.AGUARDANDO,
            date=date,
            sequence=len(self.issues) + 1
        )
        self.issues.append(issue)

    def add_works(self, description: str, time: float, work_date: str, idaction: Optional[str] = None, idissue: Optional[str] = None):
        self.needs_sync = True
        novo_work = WorkLog(
            idwork=generate_uuid(),
            idaction=idaction,
            idissue=idissue,
            description=description,
            time=time,
            date=work_date,
            sequence=len(self.works) + 1
        )
        self.works.append(novo_work)

    def del_work(self, idwork: str):
        self.needs_sync = True
        self.works = [w for w in self.works if w.idwork != idwork]

    def get_melistones_by_code(self, idmilestone: str) -> Optional[Milestones]:
        return next((milestone for milestone in self.milestones if milestone.idmilestone == idmilestone), None)
    
    def get_issue_by_code(self, idissues: str) -> Optional[Issues]:
        return next((issue for issue in self.issues if issue.idissues == idissues), None)

    def get_action_by_code(self, idaction: str) -> Optional[Action]:
        return next((action for action in self.actions if action.idaction == idaction), None)

    def list_pending_actions(self) -> List[Action]:
        return [action for action in self.actions if action.status != StatusEnum.CONCLUIDO]

    def save(self):
        self.update_milestones_status()

        path_db = get_db_dir()
        path_db.mkdir(exist_ok=True, parents=True)
        file_path = path_db / 'db.json'
        
        if file_path.exists():
            self._create_backup(file_path)
            
        file_path.write_text(self.model_dump_json(indent=4), encoding='utf-8')
        print(f"[green]Projeto salvo em {file_path}[/green]")
        return file_path

    def _create_backup(self, file_path: Path):
        import shutil
        from datetime import datetime
        backup_dir = file_path.parent
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        backup_path = backup_dir / f"db_backup_{timestamp}.json"
        
        shutil.copy(file_path, backup_path)
        
        backups = sorted(backup_dir.glob("db_backup_*.json"), key=lambda x: x.name, reverse=True)
        if len(backups) > 3:
            for old_backup in backups[3:]:
                old_backup.unlink()

    def del_milestone(self, idmilestone: str):
        self.needs_sync = True
        self.milestones = [m for m in self.milestones if m.idmilestone != idmilestone]
        for action in self.actions:
            if action.idmilestone == idmilestone:
                action.idmilestone = None

    def del_action(self, idaction: str):
        self.needs_sync = True
        self.actions = [a for a in self.actions if a.idaction != idaction]
        self.works = [w for w in self.works if w.idaction != idaction]

    def del_issue(self, idissues: str):
        self.needs_sync = True
        self.issues = [i for i in self.issues if i.idissues != idissues]

    def clear_structure(self):
        self.needs_sync = True
        self.milestones = []
        self.actions = []

    def update_milestones_status(self):
        """
        Verifica se todas as ações de cada milestone estão concluídas.
        Se sim, altera o status da milestone para '✅ Concluído'.
        """
        for milestone in self.milestones:
            # Filtra as ações pertencentes a esta milestone
            actions_in_milestone = [a for a in self.actions if a.idmilestone == milestone.idmilestone]
            
            # Se houver ações e todas estiverem concluídas, marca a milestone como concluída
            if actions_in_milestone and all(a.status == StatusEnum.CONCLUIDO for a in actions_in_milestone):
                milestone.status = StatusEnum.CONCLUIDO

    def report_projeto(self):
        report = f'# 🎯 {self.project.name}\n\n> {self.project.description}\n'
        milestonetxt = ''
        if len(self.actions) > 0:
            report += '\n## ⚡️ Actions\n\n'
            for action in self.actions:
                if action.idmilestone is not None:
                    milestone = self.get_melistones_by_code(action.idmilestone)
                    if milestone and milestonetxt != milestone.name:
                        milestonetxt = milestone.name
                        report += f'\n### 🚩 {milestonetxt}\n'
                
                check = 'x' if action.status == StatusEnum.CONCLUIDO else ' '
                report += f'- [{check}] {action.name} {action.status.value}\n'

        if len(self.issues) > 0:
            report += '\n## 🐛 Issues\n\n'
            for issue in self.issues:
                report += f'- {issue.description} {issue.status.value} - {issue.date}\n'

        report += '\n## ⏱️ Works\n\n'
        if len(self.works) > 0:
            for work in self.works:
                report += f'- {work.date}: {work.description} ({work.time}h)\n'
        else:
            report += '*Nenhum registro de trabalho ainda.*\n'

        with open('Project Report.md', 'w', encoding='utf-8') as f:
            f.write(report)
        print("[green]Relatório gerado com sucesso![/green]")

if __name__ == '__main__':
    data = ProjectData.load_or_create("Teste", "Desc")
    data.report_projeto()
