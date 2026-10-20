Как обновлять код на сервере:

- `git pull` → `docker compose up -d --build`.
- Миграции: `python manage.py migrate`.
- Статика: collectstatic.
- Перезапуск Nginx.
- Откат: git checkout <тег> + пересборка.
- Скрипт deploy.sh или make deploy.

💡 Важно помнить при деплое (Docker Сheat Sheet)
> 1. Шаблоны затирают конфигурацию: Официальный образ NGINX при каждом старте запускает скрипт `envsubst`, который берет файлы из /etc/nginx/templates/ и перезаписывает файлы в `/etc/nginx/conf.d/`. Правки нужно вносить только в исходный файл-шаблон на хост-машине, а не внутри контейнера.
> 2. Переменная окружения: Чтобы не писать длинные флаги `-f docker-compose.prod.yml`, добавьте в `.env` строку:

```env
COMPOSE_FILE=docker-compose.yml:docker-compose.prod.yml
```
> 3. Команда жесткого перезапуска для применения конфигов:
```bash
docker compose down && docker compose up -d --force-recreate 
```