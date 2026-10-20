# Обслуживание 

- Бэкап БД: pg_dump + cron.
- Бэкап media: tar -czf.
- Обновление сертификата: certbot renew --dry-run.
- Очистка Docker: docker image prune -f.
- Мониторинг: docker compose ps, logs.
## Обновление на сервере

---

> [!NOTE] 
> На сервере нужно использовать явные флаги:

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```
> [!TIP]
> Для удобства можно создать `alias`.
```bash
# ~/.bashrc на сервере
alias dcprod='docker compose -f docker-compose.yml -f docker-compose.prod.yml'
# затем:
sourse ~/.bashrc
dcprod up -d
dcprod ps
dcprod logs --tail=20 nginx
```

> [!NOTE]
> Проверяйте итоговый `config` перед запуском:
```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml config
```

## Обновление на локальном сервере

---

> [!NOTE]
> Для локальной разработки
```bash
docker compose -f docker-compose.yml -f docker-compose.override.ym. up -d
```

> Если `override` - это dev-настройки, `prod` не нужен, можно просто:
```bash
docker compose up -d
```