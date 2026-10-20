Схема и объяснение, как всё устроено:

## Компоненты

| Сервис | Образ | Порт | Назначение |
|--------|-------|------|------------|
| nginx | nginx:1.25.5 | 80, 443 | Reverse proxy, SSL, статика |
| web | Dockerfile | 8080 | uWSGI, Django HTTP |
| daphne | Dockerfile | 9001 | ASGI, WebSocket |
| db | postgres:16.2 | 5432 | База данных |
| cache | redis:7.2.4 | 6379 | Кэш, Channels |

## Поток запроса
\`\`\`
Браузер → Nginx (443) → uWSGI (web:8080) → Django
Браузер → Nginx (443, /ws/) → Daphne (9001) → Channels
\`\`\`