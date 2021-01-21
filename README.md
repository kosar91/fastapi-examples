# Fastapi examples

### Как запустить

```bash
uvicorn main:app
```

### Документация

[Swagger](http://127.0.0.1:8000/docs)

[Redoc](http://127.0.0.1:8000/redoc)


### Производительность

Запускалось приложений с одним обработчиком для чистоты эксперимента:

```bash
gunicorn main:create_app --workers 8 -b 0.0.0.0:8000 --worker-class aiohttp.GunicornUVLoopWebWorker
```

Тестировалось с помощью WRK:

```bash
wrk -t30 -c30 -d30s http://192.168.1.132:8000/posts/
```

Результаты тестов:

|Попытка|Max RPS|99 перцентиль latency|
|---|---|---|
|1|4009.48|19.11ms|
|2|5294.68|5.71ms|
|3|5302.94|5.67ms|
