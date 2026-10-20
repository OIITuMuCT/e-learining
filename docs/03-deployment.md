Как обновлять код на сервере:

- `git pull` → `docker compose up -d --build`.
- Миграции: `python manage.py migrate`.
- Статика: collectstatic.
- Перезапуск Nginx.
- Откат: git checkout <тег> + пересборка.
- Скрипт deploy.sh или make deploy.