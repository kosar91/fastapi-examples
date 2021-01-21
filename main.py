from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.responses import PlainTextResponse
from flask import Flask

app = FastAPI()
flask_app = Flask(__name__)


@flask_app.route("/flask")
def flask_main():
    return "Hello, world from Flask!"


@app.get("/fastapi", response_class=PlainTextResponse)
def fastapi_main():
    return "Hello, world from Fastapi!"


app.mount("/", WSGIMiddleware(flask_app))
