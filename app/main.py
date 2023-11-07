import time
from fastapi import Body, FastAPI, HTTPException
import asyncpg

from . import models
from .database import engine
from .routers import post, users
from .config import settings

import requests

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

POKEAPI_URL = 'https://pokeapi.co/api/v2/pokemon?limit=2000'

async def connect_to_db():
    connection_pool = await asyncpg.create_pool(
        user = settings.database_username,
        password = settings.database_password,
        database = settings.database_name,
        host = settings.database_hostname,
    )
    return connection_pool

pokemons_list = {}

app.include_router(post.router)
app.include_router(users.router)

#path operation
@app.get("/")
async def root():
    return {"message": "Welcome"}

@app.on_event("startup")
async def startup_db_client():
    app.state.db = await connect_to_db()
    pokeapi = requests.get(POKEAPI_URL)
    count = pokeapi.json()['count']
            
    async with app.state.db.acquire() as connection:
        try:
            query = "INSERT INTO pokemons (name, image, type) VALUES ($1, $2, $3)"
            
            pokeapi = requests.get(POKEAPI_URL)
            count = pokeapi.json()['count']
            print("Loading...")
            for x in range(1,200):
                pokemon_name = pokeapi.json()['results'][x]['name']
                url = pokeapi.json()['results'][x]['url']
                pokemon_url = requests.get(url)
                pokemon_image = pokemon_url.json()['sprites']['front_default']
                pokemon_type = pokemon_url.json()['types'][0]['type']['name']
                pokemons = {'name': pokemon_name,'image':pokemon_image,'type': pokemon_type}
                pokemons_list[x] = pokemons
                #print(pokemons)
                time.sleep(0.05)

            for x in range(1,200):
                #print(pokemons_list[x]['name'])
                await connection.execute(query, pokemons_list[x]['name'], pokemons_list[x]['image'], pokemons_list[x]['type'])
                time.sleep(0.01)

            return {"message": "Data Loaded successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.on_event("shutdown")
async def shutdown_db_client():
    async with app.state.db.acquire() as connection:
        try:
            query = "DELETE FROM pokemons"
            await connection.execute(query)
            return {"message": "All data deleted from the table"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
        
    await app.state.db.close()
