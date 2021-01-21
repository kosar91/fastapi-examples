import asyncpg
import typing
from fastapi import FastAPI, Request
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
    return post_data


@app.get("/posts/", tags=['Examples'], response_model=typing.List[models.Post])
async def get_posts(request: Request):
    pg_conn = request.app.pg_conn
    posts_data = await pg_conn.fetch('select id, title, content from posts')
    return posts_data


@app.get("/hello_world/", tags=['Examples'], response_model=dict)
async def hello_world():
    return {'message': 'Hello world'}
