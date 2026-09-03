from educa.educa.settings import MEDIA_URL

# Документация приложения: [Educa]

## 1. Обзор (Overview)
Краткое описание того, для чего создано приложение, какие бизнес-задачи оно решает и какова его роль в основном проекте.
Educa - платформа электронного обучения.

## 2. Установка (Installation)
Пошаговая инструкция по добавлению приложения в существующий проект.
> If you are using Linux or macOS run the following command to activate your virtual environment:
```bash
 python -m venv venv
source venv/bin/activate
```
> If you are using Windows, use the following command instead:
```bash
.\venv\Scripts\activate
```
```bash
python -m pip install Django~=5.0.4
python -m pip install Pillow==10.3.0
```

> Install redis

```python
python -m pip install redis==5.0.4
python -m pip install django-redisboard==8.4.0
```

> Installing Django REST framework
```python
    python -m pip install djangorestframework==3.15.1
```



> Create a new project using the following command:
```bash
django-admin startproject educa
```

```bash
cd educa
django-admin startapp courses
```
### 2.1. Добавление в INSTALLED_APPS
Добавьте приложение в список `INSTALLED_APPS` в файле настроек `settings.py`:
```python
INSTALLED_APPS = [
    # ...
    'courses.apps.CoursesConfig',
    'redisboard',
    'rest_framework',
]
```

### 2.2. Настройки (Settings)
Переменные и параметры, специфичные для этого приложения, которые можно переопределить в `settings.py`:
```python
# Описание настройки
# media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
LOGIN_REDIRECT_URL = reverse_lazy('student_course_list')

```

### 2.3. Миграции
Примените миграции для создания таблиц в базе данных:
```bash
python manage.py makemigrations [courses]
python manage.py migrate
python manage.py migrate redisboard
```
### 2.4. Запуск
```bash
docker run -it --rm --name redis -p 6379:6379 redis:7.2.4
python manage.py runserver --settings=educa.settings.local
```
> Чтобы каждый раз не передавать параметр --settings
```bash
export DJANGO_SETTINGS_MODULE=educa.settings.local

set DJANGO_SETTINGS_MODULE=educa.sttings.local
```

## 3. Модели данных (Database Models)
Краткое описание моделей и связей. 
* **`ModelName`**: Описание сущности (например, `Product`).
  * `field_name` (тип): Описание поля.

* **`Subject`**: Модель Предмета
  * `title` (str): Название предмета
  * `slug` (str): URL-идентификатор

* **`Course`**: Модель Курса
  * `owner` (ForeignKey): Преподаватель (User)  создавший курс
  * `subject` (ForeignKey): Внешний ключ связана с моделью `Subject`
  * `title` (str): Название курса
  * `slug` (str): URL-идентификатор
  * `overview` (str): Краткое описание курса
  * `created` (date): Дата и время создания курса

* **`Module`**: Модель Модуль курса
  * `course` (ForeignKey): Связанна с моделью `Course`
  * `title` (str): Название модуля
  * `description` (str): Описание модуля

## 4. Маршрутизация (URLs)
Список доступных эндпоинтов, предоставляемых приложением.
* `/[app_name]/` — Главная страница приложения.
* `/[app_name]/api/v1/` — Базовый путь к API.

## 5. API / Представления (Views & Endpoints)
Описание того, как приложение взаимодействует с пользователем или фронтендом. 

> Creating custom permissions

```python
from rest_framework.permissions import BasePerimission

class IsEnrolled(BasePerimission):
    def has_object_permission(self, request, view, obj):
        return obj.students.filter(id=request.user.id).exists()
```
### API Endpoints:
* **GET** `/[app_name]/api/v1/items/` 
  * *Описание:* Получение списка объектов.
  * *Ответ (успешный):* `200 OK`
  ```json
  [
    {
      "id": 1,
      "name": "Example"
    }
  ]
  ```
> courses
* **GET** `/api/subject/`
* **GET** `/api/subject/<pk>/`
  * *Описание:* Получение списка предметов(SubjectViewSet)
  *  *Ответ ():* `код ответа`

* **GET** `/api/courses/`
* **GET** `/api/courses/<pk>/`
  * *Описание:* Получение списка курсов(CourseViewSet)
  *  *Ответ ():* `код ответа`

> action
* enroll
* **POST** `/courses/<pk>/enroll/`(IsAuthenticated)
  * *Описание:* Зачисление студента на курс
  * *Ответ ():* `код ответа`
> action
* contents
* **GET** `'courses/<pk>/contents`
  *  *Описание:* Показ содержания курса(IsAuthenticated, IsEnrolled)
  *  *Ответ ():* `код ответа`



## 6. Фоновые задачи / Сигналы
Описание кастомных команд, Celery-задач или сигналов Django (`signals.py`), которые срабатывают при определенных условиях.

## 7. Развертывание и Зависимости
* Специфичные зависимости (например, библиотеки, указанные в `requirements.txt` или `pyproject.toml`).
* Особые требования к окружению (переменные среды, сторонние сервисы).

## 8. Примеры использования (Usage)
Примеры кода, демонстрирующие интеграцию или использование основных функций приложения разработчиками.

## 9. Известные проблемы / TODO
Список текущих ограничений или задач, запланированных к реализации в следующих версиях.