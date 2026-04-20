import os
import shutil
import pytest
from pathlib import Path

import app.import_project_short as ips
from app.project_data import get_db_dir

TEST_FILE = 'Project Short_TEST.md'
PROJECT_DIR = get_db_dir()
DB_FILE = PROJECT_DIR / 'db.json'

SAMPLE_CONTENT = (
    "# Test Project\n\n"
    "> This is a test project description.\n\n"
    "Action 1\nAction 2\n\n"
    "*Milestone 1\nAction 3\nAction 4\n\n"
    "*Milestone 2\nAction 5\n\n"
    "*ISSUES\nIssue 1\nIssue 2\n"
)

def setup_module(module):
    # Clean up before test
    if Path(TEST_FILE).exists():
        os.remove(TEST_FILE)
    if Path(DB_FILE).exists():
        os.remove(DB_FILE)
    if Path(PROJECT_DIR).exists():
        shutil.rmtree(PROJECT_DIR)

def teardown_module(module):
    # Clean up after test
    if Path(TEST_FILE).exists():
        os.remove(TEST_FILE)
    if Path(DB_FILE).exists():
        os.remove(DB_FILE)
    if Path(PROJECT_DIR).exists():
        shutil.rmtree(PROJECT_DIR)

def test_import_project_short_creates_db():
    # Write sample Project Short.md
    Path(TEST_FILE).write_text(SAMPLE_CONTENT, encoding='utf-8')
    # Run the import logic
    ips.main_import_project_short(TEST_FILE)
    # Check if db.json was created
    assert Path(DB_FILE).exists(), 'db.json was not created.'
    # Optionally, check contents
    content = Path(DB_FILE).read_text(encoding='utf-8')
    assert 'Test Project' in content
    assert 'This is a test project description.' in content
    # Clean up
    Path(TEST_FILE).unlink()
