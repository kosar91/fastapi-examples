import asyncpg
import typing
from fastapi import FastAPI, Request, APIRouter
from fastapi_utils.cbv import cbv

import models

app = FastAPI()
router = APIRouter(
    prefix='/posts',
)


@app.on_event("startup")
async def init_db_connection():
    #  Yes it is hardcode ;-)
    app.pg_conn = await asyncpg.connect(dsn='postgresql://postgres:postgres@0.0.0.0:5432/postgres')


@app.on_event("shutdown")
async def close_db_connection():
    await app.pg_conn.close()


@cbv(router)
class PostsCBV:
    request: Request

    @router.post("/", tags=['Examples'], response_model=models.Post)
    async def create_post(self, post: models.PostCreate):
        pg_conn = self.request.app.pg_conn
        post_data = await pg_conn.fetchrow(
            'insert into posts (title, content) values ($1, $2) RETURNING id, title, content',
            post.title, post.content
        )
        return post_data

    @router.get("/", tags=['Examples'], response_model=typing.List[models.Post])
    async def get_posts(self):
        pg_conn = self.request.app.pg_conn
        posts_data = await pg_conn.fetch('select id, title, content from posts')
        return posts_data


app.include_router(router)
