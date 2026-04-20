import os
import pytest
from pathlib import Path
import shutil

from app.import_project_short import project_init, project_update
from app.milestone_console import milestone_add, milestone_list, milestone_delete, milestone_status
from app.actions_console import action_add, action_list, action_delete, action_modify, action_status
from app.issues_console import issue_add, issue_list, issue_delete, issue_modify, issue_status
from app.issue_md_sync import sync_issues_markdown
from app.works_console import work_add, work_list, work_delete, work_report
from app.project_data import ProjectData, get_db_dir
from app.models import StatusEnum

TEST_FILE = 'Project Short_TEST_CLI.md'
DB_DIR = get_db_dir() 
DB_FILE = DB_DIR / 'db.json'
ISSUES_MD = DB_DIR / 'issues.md'

@pytest.fixture(autouse=True)
def cleanup():
    if Path(TEST_FILE).exists(): os.remove(TEST_FILE)
    if DB_DIR.exists():
        shutil.rmtree(DB_DIR)
    DB_DIR.mkdir(parents=True, exist_ok=True)
    yield
    if Path(TEST_FILE).exists(): os.remove(TEST_FILE)
    if DB_DIR.exists():
        shutil.rmtree(DB_DIR)

def test_project_init_creates_issue_template_but_no_import():
    print(f"\nDEBUG: DB_DIR={DB_DIR}")
    print(f"DEBUG: ISSUES_MD={ISSUES_MD}")
    content = "# Project\n\n> Desc\n\n* M1\nA1\n"
    Path(TEST_FILE).write_text(content, encoding='utf-8')
    # O init DEVE criar db.json e issues.md
    result = project_init(TEST_FILE)
    assert result is True
    assert DB_FILE.exists()
    assert ISSUES_MD.exists()
    
    data = ProjectData.load_or_create()
    assert len(data.issues) == 0

def test_project_init_twice_fails():
    content = "# Project\n\n> Desc\n\n* M1\nA1\n"
    Path(TEST_FILE).write_text(content, encoding='utf-8')
    project_init(TEST_FILE)
    result = project_init(TEST_FILE)
    assert result is False

def test_issues_markdown_sync():
    # Setup inicial para poder carregar ProjectData
    data = ProjectData.load_or_create("P1", "D1")
    data.save()
    
    data.add_issues("Issue CLI", "2026-04-20")
    data.save()
    sync_issues_markdown()
    assert ISSUES_MD.exists()
    
    txt = ISSUES_MD.read_text(encoding='utf-8')
    txt = txt.replace("[ ]", "[x]")
    txt += "\n- [ ] Nova Issue Manual"
    ISSUES_MD.write_text(txt, encoding='utf-8')
    
    sync_issues_markdown()
    
    data_reloaded = ProjectData.load_or_create()
    assert any(i.description == "Nova Issue Manual" for i in data_reloaded.issues)
    # A primeira issue deve estar concluída
    # Como não temos ID fixo no teste manual do MD, buscamos por texto
    cli_issue = next(i for i in data_reloaded.issues if i.description == "Issue CLI")
    assert cli_issue.status == StatusEnum.CONCLUIDO

def test_issues_deletion_syncs_markdown():
    # Setup
    data = ProjectData.load_or_create("P1", "D1")
    data.add_issues("Issue Para Deletar", "2026-04-20")
    data.save()
    sync_issues_markdown(data=data)
    assert "Issue Para Deletar" in ISSUES_MD.read_text(encoding='utf-8')
    
    # Simula o comando de console (deleta e sincroniza)
    data.del_issue(data.issues[0].idissues)
    sync_issues_markdown(data=data)
    
    # Verifica
    txt = ISSUES_MD.read_text(encoding='utf-8')
    assert "Issue Para Deletar" not in txt

def test_project_update_syncs_issues():
    content = "# Project\n\n> Desc\n\n* M1\nA1\n"
    Path(TEST_FILE).write_text(content, encoding='utf-8')
    project_init(TEST_FILE)
    
    # Adiciona uma issue no MD recém criado
    txt = ISSUES_MD.read_text(encoding='utf-8')
    txt += "\n- [ ] Issue do MD"
    ISSUES_MD.write_text(txt, encoding='utf-8')
    
    project_update(TEST_FILE)
    
    data = ProjectData.load_or_create()
    assert any(i.description == "Issue do MD" for i in data.issues)

def test_backup_retention():
    data = ProjectData.load_or_create("P1", "D1")
    for i in range(5):
        data.save()
    backups = list(DB_DIR.glob("db_backup_*.json"))
    assert len(backups) == 3
