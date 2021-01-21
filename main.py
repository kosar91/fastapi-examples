import asyncpg
import typing
from fastapi import FastAPI, Request
from fastapi.responses import UJSONResponse
import models

app = FastAPI()


@app.on_event("startup")
async def init_db_connection():
    #  Yes it is hardcode ;-)
    app.pg_conn = await asyncpg.create_pool(dsn='postgresql://postgres:postgres@0.0.0.0:5432/postgres')


@app.on_event("shutdown")
async def close_db_connection():
    await app.pg_conn.close()


@app.post("/posts/", tags=['Examples'], response_model=models.Post)
async def create_post(request: Request, post: models.PostCreate):
    pg_conn = request.app.pg_conn
    post_data = await pg_conn.fetchrow(
        'insert into posts (title, content) values ($1, $2) RETURNING id, title, content',
        post.title, post.content
    )
    return UJSONResponse(post_data)


@app.get("/posts/")
async def get_posts(request: Request):
    pg_conn = request.app.pg_conn
    posts_data = await pg_conn.fetch('select id, title, content from posts')
    posts_data = [dict(item) for item in posts_data]
    return UJSONResponse(posts_data)


@app.get("/hello_world/")
async def hello_world():
    return UJSONResponse({'message': 'Hello world'})
