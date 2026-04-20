import os
import pytest

@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    os.environ["PROJ_DB_DIR"] = ".project_test"
