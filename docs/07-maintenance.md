# Обслуживание 

- Бэкап БД: pg_dump + cron.
- Бэкап media: tar -czf.
- Обновление сертификата: certbot renew --dry-run.
- Очистка Docker: docker image prune -f.
- Мониторинг: docker compose ps, logs.