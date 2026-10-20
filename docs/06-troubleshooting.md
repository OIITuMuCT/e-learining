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