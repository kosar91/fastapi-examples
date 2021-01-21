from functools import partial

import asyncpg
import ujson
from aiohttp import web
from aiohttp.web_app import Application

json_response = partial(web.json_response, dumps=ujson.dumps)


async def init_db_connection(application):
    #  Yes it is hardcode ;-)
    application['pg_conn'] = await asyncpg.create_pool(dsn='postgresql://postgres:postgres@0.0.0.0:5432/postgres')

    async def on_shutdown(app_to_close: Application):
        await app_to_close['pg_conn'].close()

    application.on_shutdown.append(on_shutdown)


routes = web.RouteTableDef()


@routes.post('/posts/')
async def create_post(request):
    pg_conn = request.app['pg_conn']
    input_data = await request.json()
    post_data = await pg_conn.fetchrow(
        'insert into posts (title, content) values ($1, $2) RETURNING id, title, content',
        input_data['title'], input_data['content']
    )
    return json_response(dict(post_data))


@routes.get('/posts/')
async def get_posts(request):
    pg_conn = request.app['pg_conn']
    posts_data = await pg_conn.fetch('select id, title, content from posts')
    posts_data = [dict(item) for item in posts_data]
    return json_response(posts_data)


@routes.get('/hello_world/')
async def get_posts(request):
    return json_response({'message': "Hello world"})


async def create_app():
    app = Application()
    app.on_startup.append(init_db_connection)
    app.add_routes(routes)
    return app


if __name__ == '__main__':
    web.run_app(create_app(), port=8000, host='0.0.0.0')
