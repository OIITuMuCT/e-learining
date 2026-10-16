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

> !!! Error response from daemon: failed to create task for 
> container: failed to create shim task: OCI runtime 
> create failed: runc create failed: unable to start container 
> process: error during container init: 
> exec: "./wait-for-it.sh": permission denied: unknown
> Solution:
```bash
chmod +x ./wait-for-it.sh
# or Open Dockerfile and add this line before your ENTRYPOINT or CMD directive:
RUN chmod +x ./wait-for-it.sh
```
### 2.4.1. Миграции в Docker контейнере:
```bash
docker compose up
docker compose exec web python /code/educa/manage.py migrate
docker compose exec web pyhton /code/educa/manage.py createsuperuser
```

### 2.4.2. Работа с Docker контейнером:
```bash
# 1. Пересобрать и пересоздать контейнеры
docker compose up -d --build

# 2. Убедиться что все работает
docker compose ps
docker compose logs web

# 3. Убрать висячие образы (безопасно)
docker image prune -f
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

### TODO:

---

- [] Добавить имя пользователя в Navbar
- [] Добавить кнопку регистрации
- [] Добавить кнопку для создания курса(для инструкторов)
- [] Добавить отображение текстового контента в markdown
- [] Подтверждение учетной записи по email
- [x] Безопасность: скрыть важные данные из репозитория git

---

> Смена пароля для базы данных из контейнера  
```bash
docker compose exec db psql -U postgres -d postgres
```

```sql
ALTER USER postgres WITH PASSWORD 'new_password';
```
> Обновите переменную .env

```bash
docker compose up -d --force-recreate web daphne
```

```commandline
# 1. Все ли контейнеры запущены
docker compose ps

# 2. Логи проблемного сервиса
docker compose logs --tail=30 nginx
docker compose logs --tail=30 web
docker compose logs --tail=30 daphne

# 3. Проверка ответа
curl -Ik https://159.194.242.70

# 4. Если Django — проверить настройки из правильной директории
docker compose exec -w /code/educa web python -c "
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'educa.settings.prod'
import django
django.setup()
from django.conf import settings
print('ALLOWED_HOSTS:', settings.ALLOWED_HOSTS)
"
```
# Static and media

---

```
docker compose exec -w /code/educa web python manage.py collectstatic --noinput

# Ожидаемый вывод:
0 static files copied to '/code/educa/static', 172 unmodified.

```
> Проверка статики
```commandline
docker compose exec nginx ls /code/educa/static/ | head
```
```commandline
>>>
admin
css
debug_toolbar
redisboard
rest_framework

```
> Проверка отдачи статики через NGINX:
```commandline
curl -I https://vataman.ru/static/admin/css/base.css

# Response
HTTP/1.1 200 OK
Server: nginx/1.25.5
Date: Wed, 14 Oct 2026 16:28:47 GMT
Content-Type: text/css
Content-Length: 22120
Last-Modified: Wed, 14 Oct 2026 10:25:58 GMT
Connection: keep-alive
ETag: "6acf58b6-5668"
Accept-Ranges: bytes

```
### Collectstatic
```commandline
docker compose exec -w /code/educa web python manage.py collectstatic --noinput
```
> Проверка что файлы появились
```commandline
docker compose exec nginx ls /code/educa/static/ | head
docker compose exec nginx ls /code/educa/static/admin/css/ | head
```
> Проверка отдачи через Nginx:
```commandline
curl -I https://vataman.ru/static/admin/css/base.css
```
### Проверка /media/
```commandline
curl -I https://vataman.ru/media/
```
# Проверить что Nginx видит `media`
```commandline
docker compose exec nginx ls -la /code/educa/media/
```

### Права доступа

---
```commandline
chown -R 33:33 /root/elearining/educa/media
chmod 755 /root/elearining/educa/media

# чтобы хост-пользователь, и контейнер могли писать:
chmod 777 /root/elearining/educa/media
# Но 777 - не безопасно. Лучше chown на UID 33 


```
> Следующий шаг
```commandline
mkdir -p /root/elearining/educa/media
chown -R 33:33 /root/elearining/educa/media
docker compose exec nginx ls -la /code/educa/ | grep media

# ответ
drwxr-xr-x  2 www-data www-data 4096 Oct 14 16:45 media

```