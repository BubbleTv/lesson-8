"""Тесты для методов работы с проектами Yougile API"""

import pytest
import uuid
import time


class TestProjects:
    """Тесты для методов работы с проектами"""

    # ============= ТЕСТЫ ДЛЯ СОЗДАНИЯ ПРОЕКТА =============

    def test_create_project_positive(self, project_api):
        """Позитивный тест: создание проекта с валидными данными"""
        project_data = {
            "title": f"Тестовый проект {uuid.uuid4().hex[:8]}",
            "users": {}
        }

        response = project_api.create_project(project_data)

        assert "id" in response
        assert response["id"] is not None

        project_id = response["id"]
        get_response = project_api.get_project(project_id)
        assert get_response["title"] == project_data["title"]

        project_api.delete_project(project_id)

    def test_create_project_without_title_negative(self, project_api):
        """Негативный тест: создание проекта без обязательного поля title"""
        invalid_data = {"users": {}}

        with pytest.raises(Exception) as exc_info:
            project_api.create_project(invalid_data)

        assert "400" in str(exc_info.value) or "error" in str(exc_info.value).lower()

    def test_create_project_with_empty_title_negative(self, project_api):
        """Негативный тест: создание проекта с пустым title"""
        invalid_data = {"title": "", "users": {}}

        with pytest.raises(Exception):
            project_api.create_project(invalid_data)

    # ============= ТЕСТЫ ДЛЯ ПОЛУЧЕНИЯ ПРОЕКТА =============

    def test_get_project_positive(self, project_api, created_project):
        """Позитивный тест: получение существующего проекта по ID"""
        response = project_api.get_project(created_project)

        assert "id" in response
        assert response["id"] == created_project
        assert "title" in response
        assert "timestamp" in response

    def test_get_project_with_invalid_id_negative(self, project_api):
        """Негативный тест: получение проекта с несуществующим ID"""
        fake_id = str(uuid.uuid4())

        with pytest.raises(AssertionError) as exc_info:
            project_api.get_project_expect_error(fake_id)

        assert "404" in str(exc_info.value)

    def test_get_project_with_malformed_id_negative(self, project_api):
        """Негативный тест: получение проекта с некорректным форматом ID"""
        invalid_ids = ["123", "not-a-uuid", "abc"]

        for invalid_id in invalid_ids:
            with pytest.raises(Exception):
                project_api.get_project(invalid_id)

    def test_get_project_with_empty_id_negative(self, project_api):
        """Негативный тест: получение проекта с пустым ID"""
        with pytest.raises(Exception):
            project_api.get_project("")

    # ============= ТЕСТЫ ДЛЯ ОБНОВЛЕНИЯ ПРОЕКТА =============

    def test_update_project_title_positive(self, project_api, created_project):
        """Позитивный тест: обновление названия проекта"""
        new_title = f"Обновленный проект {uuid.uuid4().hex[:8]}"
        update_data = {"title": new_title}

        response = project_api.update_project(created_project, update_data)

        assert "id" in response
        assert response["id"] == created_project

        get_response = project_api.get_project(created_project)
        assert get_response["title"] == new_title

    def test_update_project_with_deleted_flag_positive(self, project_api, created_project):
        """Позитивный тест: удаление проекта через поле deleted"""
        update_data = {"deleted": True}

        response = project_api.update_project(created_project, update_data)

        assert "id" in response
        assert response["id"] == created_project

        get_response = project_api.get_project(created_project)
        assert get_response.get("deleted") is True

    def test_update_nonexistent_project_negative(self, project_api):
        """Негативный тест: обновление несуществующего проекта"""
        fake_id = str(uuid.uuid4())
        update_data = {"title": "Новое название"}

        with pytest.raises(Exception) as exc_info:
            project_api.update_project(fake_id, update_data)

        assert "404" in str(exc_info.value)

    def test_update_project_with_invalid_field_negative(self, project_api, created_project):
        """Негативный тест: обновление проекта с невалидным полем"""
        invalid_update_data = {"invalid_field_xyz": "some_value"}

        with pytest.raises(AssertionError) as exc_info:
            project_api.update_project(created_project, invalid_update_data)

        error_msg = str(exc_info.value)
        assert "400" in error_msg
        assert "should not exist" in error_msg

    # ============= ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ =============

    def test_create_multiple_projects_positive(self, project_api):
        """Позитивный тест: создание нескольких проектов подряд"""
        project_ids = []

        try:
            for i in range(3):
                project_data = {
                    "title": f"Проект {i+1} {uuid.uuid4().hex[:6]}",
                    "users": {}
                }

                response = project_api.create_project(project_data)
                assert "id" in response
                project_ids.append(response["id"])
                time.sleep(0.5)

            for project_id in project_ids:
                get_response = project_api.get_project(project_id)
                assert get_response["id"] == project_id

        finally:
            for project_id in project_ids:
                try:
                    project_api.delete_project(project_id)
                except Exception:
                    pass

    def test_create_project_with_long_title_positive(self, project_api):
        """Позитивный тест: создание проекта с длинным названием"""
        long_title = "О" * 100
        project_data = {"title": long_title, "users": {}}

        response = project_api.create_project(project_data)

        assert "id" in response
        project_id = response["id"]

        get_response = project_api.get_project(project_id)
        assert get_response["title"] == long_title

        project_api.delete_project(project_id)

    def test_create_project_with_special_characters_positive(self, project_api):
        """Позитивный тест: создание проекта с спецсимволами в названии"""
        special_title = "Проект!@#$%^&*()_+{}[]|\\:;\"'<>,.?/~`"
        project_data = {"title": special_title, "users": {}}

        response = project_api.create_project(project_data)

        assert "id" in response
        project_id = response["id"]

        get_response = project_api.get_project(project_id)
        assert get_response["title"] == special_title

        project_api.delete_project(project_id)

    def test_update_project_title_to_empty_negative(self, project_api, created_project):
        """Негативный тест: обновление названия проекта на пустую строку"""
        update_data = {"title": ""}

        with pytest.raises(Exception):
            project_api.update_project(created_project, update_data)