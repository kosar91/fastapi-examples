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
uvicorn main:app --workers 1 --log-level warning
```

Тестировалось с помощью Yandex tank:

```bash
docker run \
    -v $(pwd):/var/loadtest \
    -v $SSH_AUTH_SOCK:/ssh-agent -e SSH_AUTH_SOCK=/ssh-agent \
    --net host \
    -it direvius/yandex-tank \
    -c tank-config.yaml
```

Результаты тестов:

|Попытка|Средний RPS|Средний latency|
|---|---|---|
|1|1281.79|23.40ms|

