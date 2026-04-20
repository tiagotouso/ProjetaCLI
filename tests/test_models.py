import pytest
from pydantic import ValidationError
from app.models import Project, Milestones, Action, Issues, WorkLog, StatusEnum

# Fixtures for Project
@pytest.fixture
def project_data():
    return {
        "idproject": "PROJ-001",
        "name": "Test Project",
        "description": "This is a test project",
        "status": StatusEnum.INICIADO
    }

@pytest.fixture
def project(project_data):
    return Project(**project_data)

def test_project_idproject(project, project_data):
    assert project.idproject == project_data["idproject"]

def test_project_name(project, project_data):
    assert project.name == project_data["name"]

def test_project_description(project, project_data):
    assert project.description == project_data["description"]

def test_project_status(project, project_data):
    assert project.status == project_data["status"]

def test_project_invalid_status():
    with pytest.raises(ValidationError):
        Project(
            idproject="PROJ-002",
            name="Invalid Status Project",
            description="This project has an invalid status",
            status="INVALID_STATUS"
        )

def test_project_missing_required_field():
    with pytest.raises(ValidationError):
        Project(name="Missing idproject", description="some description", status=StatusEnum.INICIADO)

# Fixtures for Milestones
@pytest.fixture
def milestone_data():
    return {
        "idmilestone": "MILE-001",
        "name": "Test Milestone",
        "status": StatusEnum.CONCLUIDO,
        "sequence": 1
    }

@pytest.fixture
def milestone(milestone_data):
    return Milestones(**milestone_data)

def test_milestone_idmilestone(milestone, milestone_data):
    assert milestone.idmilestone == milestone_data["idmilestone"]

def test_milestone_name(milestone, milestone_data):
    assert milestone.name == milestone_data["name"]

def test_milestone_status(milestone, milestone_data):
    assert milestone.status == milestone_data["status"]

# Fixtures for Action
@pytest.fixture
def action_data():
    return {
        "idmilestone": "MILE-001",
        "idaction": "ACT-001",
        "name": "Test Action",
        "status": StatusEnum.AGUARDANDO,
        "sequence": 1
    }

@pytest.fixture
def action(action_data):
    return Action(**action_data)

def test_action_idmilestone(action, action_data):
    assert action.idmilestone == action_data["idmilestone"]

def test_action_idaction(action, action_data):
    assert action.idaction == action_data["idaction"]

def test_action_name(action, action_data):
    assert action.name == action_data["name"]

def test_action_status(action, action_data):
    assert action.status == action_data["status"]

# Fixtures for Action without Milestone
@pytest.fixture
def action_without_milestone_data():
    return {
        "idaction": "ACT-002",
        "name": "Action without Milestone",
        "status": StatusEnum.CANCELADO,
        "sequence": 1
    }

@pytest.fixture
def action_without_milestone(action_without_milestone_data):
    return Action(**action_without_milestone_data)

def test_action_without_milestone_idmilestone(action_without_milestone):
    assert action_without_milestone.idmilestone is None

def test_action_without_milestone_idaction(action_without_milestone, action_without_milestone_data):
    assert action_without_milestone.idaction == action_without_milestone_data["idaction"]

def test_action_without_milestone_name(action_without_milestone, action_without_milestone_data):
    assert action_without_milestone.name == action_without_milestone_data["name"]

def test_action_without_milestone_status(action_without_milestone, action_without_milestone_data):
    assert action_without_milestone.status == action_without_milestone_data["status"]

# Fixtures for Issues
@pytest.fixture
def issue_data():
    return {
        "idissues": "ISSUE-001",
        "description": "Test Issue",
        "status": StatusEnum.INICIADO,
        "date": "2025-07-29",
        "sequence": 1
    }

@pytest.fixture
def issue(issue_data):
    return Issues(**issue_data)

def test_issue_idissues(issue, issue_data):
    assert issue.idissues == issue_data["idissues"]

def test_issue_description(issue, issue_data):
    assert issue.description == issue_data["description"]

def test_issue_status(issue, issue_data):
    assert issue.status == issue_data["status"]

def test_issue_date(issue, issue_data):
    assert issue.date == issue_data["date"]

# Fixtures for WorkLog
@pytest.fixture
def worklog_data():
    return {
        "idwork": "WL-001",
        "idaction": "ACT-001",
        "description": "Test WorkLog",
        "time": 2.5,
        "date": "2025-07-29",
        "sequence": 1
    }

@pytest.fixture
def worklog(worklog_data):
    return WorkLog(**worklog_data)

def test_worklog_code(worklog, worklog_data):
    assert worklog.idwork == worklog_data["idwork"]

def test_worklog_description(worklog, worklog_data):
    assert worklog.description == worklog_data["description"]

def test_worklog_time(worklog, worklog_data):
    assert worklog.time == worklog_data["time"]

def test_worklog_date(worklog, worklog_data):
    assert worklog.date == worklog_data["date"]

