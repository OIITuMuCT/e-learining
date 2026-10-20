# Educa Project

Django-приложение для онлайн-обучения с чатом (WebSocket), HTTPS и Docker.

## Стек
- Django 5.2 LTS, Python 3.12
- PostgreSQL 16.2, Redis 7.2.4
- Nginx 1.25.5, uWSGI, Daphne
- Docker Compose, Let's Encrypt

## Быстрый старт
\`\`\`bash
git clone git@github.com:user/educa.git
cd educa
cp .env.example .env
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
\`\`\`

## Документация
- [Быстрый старт](docs/01-getting-started.md)
- [Архитектура](docs/02-architecture.md)
- [Деплой](docs/03-deployment.md)
- [Настройки](docs/04-configuration.md)
- [Разработка](docs/05-development.md)
- [Решение проблем](docs/06-troubleshooting.md)