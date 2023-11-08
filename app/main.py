from fastapi import Body, FastAPI, HTTPException, Request, Response
from fastapi.responses import PlainTextResponse

import asyncpg

from . import models
from .database import engine
from .routers import get, users, auth
from .config import settings

import httpx

from contextlib import asynccontextmanager
from fastapi.responses import StreamingResponse
from starlette.background import BackgroundTask

models.Base.metadata.create_all(bind=engine)

async def connect_to_db():
    connection_pool = await asyncpg.create_pool(
        user = settings.database_username,
        password = settings.database_password,
        database = settings.database_name,
        host = settings.database_hostname,
    )
    return connection_pool

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db = await connect_to_db()
    async with httpx.AsyncClient() as client:
        yield {'client': client}
        await app.state.db.close()

app = FastAPI(lifespan=lifespan)

POKEAPI_URL = 'https://pokeapi.co/api/v2/pokemon?limit=2000'

pokemons_list = {}

app.include_router(get.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get('/')
async def home(request: Request):
    client = request.state.client
    req = client.build_request('GET', POKEAPI_URL)
    r = await client.send(req)
    count = r.json()['count']
    
    for x in range(1,count):
        pokemon_name = r.json()['results'][x]['name']
        url = r.json()['results'][x]['url']
        req_url = client.build_request('GET', url)
        r_url = await client.send(req_url)
        pokemon_image = r_url.json()['sprites']['front_default']
        pokemon_type = r_url.json()['types'][0]['type']['name']
        pokemons = {'name': pokemon_name,'image':pokemon_image,'type': pokemon_type}
        pokemons_list[x] = pokemons
        async with app.state.db.acquire() as connection:
            query = "INSERT INTO pokemons (name, image, type) VALUES ($1, $2, $3)"
            await connection.execute(query, pokemons_list[x]['name'], pokemons_list[x]['image'], pokemons_list[x]['type'])
        print(pokemons)
    return pokemons_list
