"""API для работы с проектами Yougile"""


class ProjectAPI:
    """Класс для работы с проектами в Yougile API"""

    def __init__(self, api_client):
        self.api_client = api_client
        self.base_endpoint = "projects"

    def create_project(self, project_data):
        """Создание проекта"""
        return self.api_client.post(self.base_endpoint, project_data)

    def get_project(self, project_id):
        """Получение проекта по ID"""
        endpoint = f"{self.base_endpoint}/{project_id}"
        return self.api_client.get(endpoint)

    def update_project(self, project_id, update_data):
        """Обновление проекта"""
        endpoint = f"{self.base_endpoint}/{project_id}"
        return self.api_client.put(endpoint, update_data)

    def delete_project(self, project_id):
        """Удаление проекта (через обновление поля deleted)"""
        endpoint = f"{self.base_endpoint}/{project_id}"
        update_data = {"deleted": True}
        return self.api_client.put(endpoint, update_data)

    def get_project_expect_error(self, project_id):
        """Получение проекта с ожиданием ошибки"""
        endpoint = f"{self.base_endpoint}/{project_id}"
        return self.api_client.get(endpoint, expected_status=404)