#!/bin/bash
echo "🚀 Начало деплоя..."

git pull origin main
docker compose build --pull
docker compose run --rm web python /code/educa/manage.py migrate
docker compose run --rm web python /code/educa/manage.py collectstatic --noinput
docker compose up -d --no-deps --force-recreate

echo "✨ Деплой успешно завершен!"
