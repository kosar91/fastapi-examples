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
gunicorn main:create_app --workers 1 -b 0.0.0.0:8000 --worker-class aiohttp.GunicornUVLoopWebWorker
```

Тестировалось с помощью WRK:

```bash
docker run \
    -v $(pwd):/var/loadtest \
    -v $SSH_AUTH_SOCK:/ssh-agent -e SSH_AUTH_SOCK=/ssh-agent \
    --net host \
    -it direvius/yandex-tank \
    -c tank-config.yaml
```

Результаты тестов:

|Попытка|Max RPS|99 перцентиль latency|
|---|---|---|
|1|1740|11ms|
|2|1730|16ms|
|3|1690|11ms|
