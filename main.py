import typing
from fastapi import FastAPI, Response, Header, Depends, File, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from models import Post

app = FastAPI()


@app.get("/xml_example/", tags=['Examples'])
async def xml_example():
    data = """<?xml version="1.0"?>
    <posts>
        <Post id="1">
            <title>Example 1.</title>
            <content>Content 1.</title>
        </Post>
    </posts>
    """
    return Response(content=data, media_type="application/xml")


@app.get("/query_example/", tags=['Examples'], response_model=typing.List[Post])
async def query_example(skip: int = None, limit: int = None, user_agent: str = Header(None)):
    # Do some work...
    return [
        {
            'id': 1,
            'title': 'My title 1',
            'content': 'My content 1',
        },
    ]


class CommonQueryArgs(BaseModel):
    search: int = None
    skip: int = None
    limit: int = None


@app.get("/dependency_example/", tags=['Examples'], response_model=typing.List[Post])
async def dependency_example(query_args: CommonQueryArgs = Depends(CommonQueryArgs), user_agent: str = Header(None)):
    return [
        {
            'id': 1,
            'title': 'My title 1',
            'content': 'My content 1',
        },
    ]


MAX_FILE_SIZE = 1024 * 1024 * 25


@app.post("/file_upload_example/", tags=['Examples'])
async def file_upload_example(file1: bytes = File(None, max_length=MAX_FILE_SIZE), file2: UploadFile = File(None)):
    # Do some work...
    return "File uploaded successfully."


@app.get("/streaming_example", tags=['Examples'])
async def streaming_example():
    async def fake_video_streamer():
        for i in range(10):
            yield b"some fake video bytes"

    return StreamingResponse(fake_video_streamer())
