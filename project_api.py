class ProjectAPI:
    """Класс для работы с проектами в Yougile API"""
    
    def __init__(self, api_client):
        self.api_client = api_client
        self.base_endpoint = "projects"
    
    def create_project(self, project_data):
        """
        Создание проекта
        
        Позитивный сценарий: ожидаем 201 статус и ID проекта
        Негативный сценарий: ожидаем ошибку
        """
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
    
    def get_nonexistent_project(self, project_id):
        """Получение несуществующего проекта (для негативных тестов)"""
        endpoint = f"{self.base_endpoint}/{project_id}"
        return self.api_client.get(endpoint, expected_status=404)
    
    def create_project_with_invalid_data(self, invalid_data):
        """Создание проекта с невалидными данными"""
        try:
            return self.api_client.post(self.base_endpoint, invalid_data, expected_status=400)
        except AssertionError as e:
           
            if "400" not in str(e) and "422" not in str(e):
                raise
            return {"error": str(e)}