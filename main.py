import typing
from fastapi import FastAPI, HTTPException, APIRouter
from starlette import status
import models
from example_data import posts

app = FastAPI()
router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.post("/", response_model=models.Post, status_code=status.HTTP_201_CREATED)
async def create_post(post: models.PostCreate):
    """Create post."""
    post_id = max(posts.keys()) + 1
    posts[post_id] = post.dict()
    posts[post_id]['id'] = post_id
    return posts[post_id]


@router.put("/{post_id}/", response_model=models.Post)
async def update_post(post_id: int, post: models.PostUpdate):
    if post_id not in posts:
        raise HTTPException(status_code=404, detail="Item not found")

    posts[post_id].update(post.dict(exclude_unset=True))
    return posts[post_id]


@router.get("/", response_model=typing.List[models.Post])
async def get_posts():
    return list(posts.values())


@router.get("/{post_id}/", response_model=models.Post)
async def get_post(post_id: int):
    if post_id not in posts:
        raise HTTPException(status_code=404, detail="Item not found")
    return posts[post_id]


@router.delete("/{post_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int):
    return posts.pop(post_id)


app.include_router(router)
