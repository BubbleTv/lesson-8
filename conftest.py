"""Фикстуры pytest для тестов Yougile API"""

import pytest
import uuid
from api_client import YougileAPIClient
from project_api import ProjectAPI
from config import Config


@pytest.fixture(scope="session")
def api_client():
    """Фикстура для создания клиента API"""
    return YougileAPIClient(Config.BASE_URL, Config.API_KEY)


@pytest.fixture(scope="session")
def project_api(api_client):
    """Фикстура для работы с проектами"""
    return ProjectAPI(api_client)


@pytest.fixture
def created_project(project_api):
    """Фикстура для создания проекта перед тестом и удаления после"""
    project_data = {
        "title": f"Тестовый проект {uuid.uuid4().hex[:8]}",
        "users": {}
    }

    response = project_api.create_project(project_data)
    project_id = response.get("id")

    yield project_id

    if project_id:
        try:
            project_api.delete_project(project_id)
        except Exception:
            pass