# Settings
Все переменные .env с описанием:

| Переменная | Обязательна | Пример | Описание |
|------------|-------------|--------|----------|
| DJANGO_SETTINGS_MODULE | Да | educa.settings.prod | Модуль настроек |
| SECRET_KEY | Да | (50 символов) | Ключ Django |
| ALLOWED_HOSTS | Да | vataman.ru,www.vataman.ru | Разрешённые хосты |
| POSTGRES_PASSWORD | Да | strong-password | Пароль БД |
| DEBUG | Нет | False | Режим отладки |