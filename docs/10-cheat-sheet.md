## Conventional Commits

---

- `feat`: — Всё, что касается создания новой бизнес-логики (новые эндпоинты, новые модели, новые вьюхи).
- `fix`: — Исправление багов (например, падение API при пустом запросе, ошибка в сериализаторе).
- `chore`: — Настройка окружения (обновление settings.py, добавление библиотек, конфигурация Docker/Nginx, миграции БД).
- `docs`: — Только документация (комментарии в коде, docstrings, файлы README.md, OpenAPI/Swagger схемы).
- `test`: — Написание или исправление тестов (pytest, django.test).
- `style`: — Правки форматирования, которые не меняют логику кода (пробелы, кавычки, исправления по PEP 8).

---

- `refactor:` — изменение кода, которое не исправляет ошибку и не добавляет новую функцию. Например, вы переписали старую громоздкую функцию на более красивую и быструю, но для пользователя ничего не изменилось.
- `perf:` — изменения, направленные строго на повышение производительности. Например, вы добавили select_related() или prefetch_related() в запрос Django, чтобы избавиться от проблемы N+1 и ускорить загрузку страницы.
- `ci:` — изменения в конфигурационных файлах и скриптах автоматизации. Например, правка файлов .github/workflows/ci.yml, о которых мы говорили раньше.
- `build:` — изменения, влияющие на систему сборки или внешние зависимости (хотя в мире Python это часто объединяют с chore). Например, переход с pip на Poetry или настройка setup.py.


## 🚀 Инициализация и Настройка (chore / docs)

---
- `chore(settings):` `initial django project layout` — базовая структура проекта после startproject.
- `chore(deps):` `add core dependencies to requirements.txt` — добавление библиотек в файл зависимостей.
- `chore(deps):` `update requirements.txt` — обновление версий пакетов.
- `chore(docker):` `add Dockerfile and docker-compose` — добавление файлов контейнеризации.
- `chore(git):` `add gitignore` — создание или обновление файла .gitignore.
- `docs(readme):` `update installation and setup instructions` — обновление инструкции по запуску в README.md.

## 🐛 Исправление багов (fix)

---
- `fix(api):` `fix internal server error on empty request` — исправление падения (ошибки 500) при пустом запросе.
- `fix(auth):` `fix token expiration time issue` — исправление бага со сроком жизни JWT-токенов.
- `fix(models):` `fix field validation error` — исправление валидации полей в БД.
- `fix(serializers):` `fix KeyError in validation logic` — исправление ошибки ключа в сериализаторе DRF.
- `fix(cors):` `fix CORS headers configuration for frontend` — исправление блокировки запросов от фронтенда.

## 🧹 Рефакторинг и Оптимизация (refactor / perf)

---
- `refactor(views):` `clean up redundant logic` — удаление дублирующегося или старого кода из вьюх.
- `perf(db):` `use select_related to fix N+1 query issue` — оптимизация запросов к базе данных (избавление от N+1).
- `perf(api):` `implement redis caching for heavy endpoints` — ускорение тяжелых эндпоинтов с помощью кэша Redis.


## 🎨 Красота, Тесты и Автоматизация (style / test / ci)

---
- `style(settings):` `improve PEP 8 formatting` — исправление отступов, пробелов и переносов строк.
- `test(app_name):` `add unit tests for api views` — написание тестов для проверки API.
- `ci(github):` `add workflow for automated testing` — настройка автотестов в GitHub Actions при Pull Request.

---


## 💡 4 золотых правила для текста коммита:

1. Пишите в повелительном наклонении `(Imperative mood):` Пишите `add`, а не ~~added~~ или ~~adds~~. Представьте, что вы даете команду `Git: (Git,)` `implement login...` (реализуй логин), `fix bug...` (исправь баг).
2. Только строчные буквы: Сам текст сообщения (после двоеточия) пишется с маленькой буквы и без точки на конце.
3. Краткость: Длина первой строки коммита не должна превышать 50-72 символов.
4. Указывайте контекст `(scope):` Всегда пишите в скобках название приложения или модуля, который вы трогали, например: `feat(users):` ... или `fix(models):` .... Это делает лог невероятно читаемым.