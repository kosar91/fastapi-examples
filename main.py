import typing
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from starlette import status

app = FastAPI()


class PostCreate(BaseModel):
    title: str
    content: str


class PostUpdate(BaseModel):
    title: typing.Optional[str]
    content: typing.Optional[str]


class Post(BaseModel):
    id: int
    title: str
    content: str


posts = {
    1: {
        'id': 1,
        'title': 'My title 1',
        'content': 'My content 1',
    },
    2: {
        'id': 2,
        'title': 'My title 2',
        'content': 'My content 2',
    }
}


@app.post("/posts/", response_model=Post)
async def create_post(post: PostCreate):
    post_id = max(posts.keys()) + 1
    posts[post_id] = post.dict()
    posts[post_id]['id'] = post_id
    return posts[post_id]


@app.put("/posts/{post_id}/", response_model=Post)
async def update_post(post_id: int, post: PostUpdate):
    if post_id not in posts:
        raise HTTPException(status_code=404, detail="Item not found")

    posts[post_id].update(post.dict(exclude_unset=True))
    return posts[post_id]


@app.get("/posts/", response_model=typing.List[Post])
async def get_posts():
    return list(posts.values())


@app.get("/posts/{post_id}/", response_model=Post)
async def get_post(post_id: int):
    if post_id not in posts:
        raise HTTPException(status_code=404, detail="Item not found")
    return posts[post_id]


@app.delete("/posts/{post_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    return posts.pop(post_id)
