🛠️ Troubleshooting: Решение ошибок 502/504/499 в связке NGINX + uWSGI + Daphne (Docker)

1. Конфликт протоколов uWSGI (Ошибки 502 Bad Gateway / 499 / 504)
• В логах NGINX: upstream prematurely closed connection while reading response header from upstream... или таймауты 504 Gateway Time-out / 499 Client Closed Request.
• В логах контейнера web (uWSGI): `uwsgi_proto_http_parser()` -> `client closed connection.`

Решение
> Перевести связку на родной бинарный сокет uWSGI (это производительнее и стабильнее внутри Docker).

1. В `docker-compose.prod.yml` (секция `web` -> `command`) принудительно запустить uWSGI в режиме `--socket`:

```yaml
command: [ "./wait-for-it.sh", "db:5432", "--",
           "uwsgi", "--socket", "0.0.0.0:8080", "--ini", "/code/config/uwsgi/uwsgi.ini" ]
```
2. В `uwsgi.ini` убедиться, что порт слушается через `socket`, а не `http-socket`:
```ini
socket = 0.0.0.0:8080
```
3. В файле-шаблоне NGINX использовать `uwsgi_pass` вместо `proxy_pass`:

```nginx
location / {
    uwsgi_pass uwsgi_app;
    include    /etc/nginx/uwsgi_params;
    # Обязательные заголовки для Django ALLOWED_HOSTS
    uwsgi_param HTTP_HOST $host;
    uwsgi_param HTTP_X_REAL_IP $remote_addr;
    uwsgi_param HTTP_X_FORWARDED_FOR $proxy_add_x_forwarded_for;
    uwsgi_param HTTP_X_FORWARDED_PROTO $scheme;
}
```

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