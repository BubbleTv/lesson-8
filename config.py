class Config:
    """Конфигурация для тестов"""
    # Базовый URL API
    BASE_URL = "https://ru.yougile.com/api-v2"
    
    # Ваш API ключ
    API_KEY = "HoiXOtBqm85so3XkGyLFXQGR5yuxoRI4gATvqQqORiZ1m1K5i0PVQSypBdruk4Ok"
    
    # Данные для тестов
    TEST_PROJECT_TITLE = "Автотест проект"
    
    # ID пользователя для тестов (если нужно добавить пользователя в проект)
    # Вы можете найти ID пользователя в ответе API или в интерфейсе Yougile
    TEST_USER_ID = None  # Оставьте None, если не нужно тестировать добавление пользователей