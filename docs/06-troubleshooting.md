Самый ценный раздел. Соберите все ошибки, с которыми столкнулись:
## 502 Bad Gateway
**Причина:** Nginx не видит uWSGI/Daphne.
**Решение:**
1. `docker compose logs nginx` — ищите `Connection refused`.
2. Проверить, слушает ли web порт: `ss -tlnp | grep 8080`.
3. Перезапустить: `docker compose restart nginx`.

## TabError: inconsistent use of tabs and spaces
**Причина:** смешаны табы и пробелы в Python.
**Решение:** `sed -i 's/\t/    /g' file.py` или `nano -T 4`.

## host not found in upstream "daphne:9001"
**Причина:** Nginx резолвит daphne при старте, а его ещё нет.
**Решение:** `resolver 127.0.0.11` + `set $daphne_upstream` + `proxy_pass $daphne_upstream`.

## 🔧 Проблема: 502 Bad Gateway после обновления проекта
Симптомы Сайт отдаёт 502 Bad Gateway.

В логах Nginx: connect() failed (111: Connection refused).

В логах web: bind(): Address already in use [core/socket.c line 769], probably another instance of uWSGI is running on the same address (0.0.0.0:8080).

Контейнер web в статусе Restarting (1).

## Причина
Цепочка из трёх взаимосвязанных проблем:

Конфликт --http и http-socket. В docker-compose.prod.yml в command был указан --http 0.0.0.0:8081, а в uwsgi.ini — http-socket = 0.0.0.0:8080. uWSGI пытался занять оба порта, что приводило к Address already in use.

Код «вшит» в образ. В docker-compose.prod.yml у сервиса web нет volume .:/code. Код (включая uwsgi.ini) копируется в образ через COPY . . в Dockerfile. Правки на хосте не применяются без пересборки образа (--build).

Nginx резолвил web через системный DNS. В upstream uwsgi_app было server web:8081, но resolver 127.0.0.11 (Docker DNS) не действует на блок upstream. Nginx резолвил web при старте через системный 127.0.0.53, получал заглушку 127.0.53.53 и пытался туда подключиться → Connection refused.

## Решение
1. Убрать конфликт портов. Оставить что-то одно:

Либо --http 0.0.0.0:8081 в command (и закомментировать http-socket в uwsgi.ini).

Либо http-socket = 0.0.0.0:8081 в uwsgi.ini (и убрать --http из command).

2. Пересобрать образ web. Так как кода в volume нет, изменения в uwsgi.ini и command применяются только через пересборку:

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml down web
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build --force-recreate web 
```
3. Перевести Nginx на переменную в proxy_pass. Убрать upstream uwsgi_app и использовать resolver + переменную:

```nginx

# nginx
location / {
    resolver 127.0.0.11 valid=10s;
    set $uwsgi_upstream "http://web:8081";
    proxy_pass $uwsgi_upstream;

    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

resolver 127.0.0.11 — внутренний DNS Docker. valid=10s — кэш на 10 секунд, чтобы при пересоздании web Nginx быстро подхватывал новый IP. Переменная в proxy_pass заставляет Nginx резолвить web при каждом запросе, а не при старте.

# 🛠️ Полезные команды для диагностики

```bash
# Статус контейнеров
docker compose -f docker-compose.yml -f docker-compose.prod.yml ps

# Логи Nginx (точная ошибка upstream)
docker compose -f docker-compose.yml -f docker-compose.prod.yml logs --tail=20 nginx

# Логи web (порт, Address already in use)
docker compose -f docker-compose.yml -f docker-compose.prod.yml logs --tail=20 web

# Что слушает web внутри
docker compose -f docker-compose.yml -f docker-compose.prod.yml exec web ss -tlnp | grep ':808'

# Куда проксирует Nginx
docker compose -f docker-compose.yml -f docker-compose.prod.yml exec nginx grep -r "proxy_pass\|resolver" /etc/nginx/conf.d/
```