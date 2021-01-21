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

Тестировалось с помощью WRK:

```bash
wrk -t30 -c30 -d30s http://localhost:8000/posts/
```

Результаты тестов:

|Попытка|Средний RPS|Средний latency|
|---|---|---|
|1|1810.54|16ms|
|2|1815.47|16ms|
|3|1841.29|16ms|
