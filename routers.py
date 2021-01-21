import typing
from fastapi import APIRouter, Request, Depends

import models

router = APIRouter(
    prefix='/posts',
)


def pg_connection(request: Request):
    return request.app.pg_conn


class PostPostgresRepository:
    def __init__(self, pg_conn=Depends(pg_connection)):
        self.pg_conn = pg_conn

    async def create_post(self, post: models.PostCreate):
        post_data = await self.pg_conn.fetchrow(
            'insert into posts (title, content) values ($1, $2) RETURNING id, title, content',
            post.title, post.content
        )
        return post_data

    async def get_posts(self):
        post_data = await self.pg_conn.fetch('select id, title, content from posts')
        return post_data


@router.post("/", tags=['Examples'], response_model=models.Post)
async def create_post(
    post: models.PostCreate,
    post_repository: PostPostgresRepository = Depends(PostPostgresRepository),
):
    return await post_repository.create_post(post)


@router.get("/", tags=['Examples'], response_model=typing.List[models.Post])
async def get_posts(post_repository: PostPostgresRepository = Depends(PostPostgresRepository)):
    return await post_repository.get_posts()
