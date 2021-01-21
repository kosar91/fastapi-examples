import asyncpg
from fastapi import FastAPI
import routers

app = FastAPI()
app.include_router(routers.router)


@app.on_event("startup")
async def init_db_connection():
    #  Yes it is hardcode ;-)
    app.pg_conn = await asyncpg.connect(dsn='postgresql://postgres:postgres@0.0.0.0:5432/postgres')


@app.on_event("shutdown")
async def close_db_connection():
    await app.pg_conn.close()
