from typing import Optional, List
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import asyncio
import asyncpg

import psycopg2
from psycopg2.extras import RealDictCursor
import time

from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post, users
from .config import settings

import requests

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

async def connect_to_db():
    connection_pool = await asyncpg.create_pool(
        user="postgres",
        password="pukar123#",
        database="fastapi",
        host="localhost",
    )
    return connection_pool

pokemons_list = {}

# my_posts = [{
#     "title": "Titile of post 1",
#     "content": "cotent of post 1 ",
#     "id":1},
#     {"title": "Top cars",
#     "content": "Check out this awesome cars",
#     "id": 2}]

# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p

app.include_router(post.router)
app.include_router(users.router)

#path operation
@app.get("/")
async def root():
    return {"message": "Welcome"}

@app.on_event("startup")
async def startup_db_client():
    app.state.db = await connect_to_db()
    
    # pokeapi = requests.get('https://pokeapi.co/api/v2/pokemon?limit=2000')
    # # data_pokemons = pokemons.text
    # # parse_json = json.loads(data_pokemons)
    # parse_json = pokeapi.json()
    # count = pokeapi.json()['count']
    
    # for x in range(1,50):
    #     pokemon_name = pokeapi.json()['results'][x]['name']
    #     url = pokeapi.json()['results'][x]['url']
    #     pokemon_url = requests.get(url)
    #     pokemon_image = pokemon_url.json()['sprites']['front_default']
    #     pokemon_type = pokemon_url.json()['types'][0]['type']['name']
    #     pokemons = {'name': pokemon_name,'image':pokemon_image,'type': pokemon_type}
    #     pokemons_list[x] = pokemons
    #     #pokemons_list.append(pokemons)
    # print(pokemons_list)

@app.on_event("shutdown")
async def shutdown_db_client():
    await app.state.db.close()

# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     return {"sucess":"sdf"}
    
@app.get("/get_data")
async def get_data():
    async with app.state.db.acquire() as connection:
        query = "SELECT * FROM users"
        result = await connection.fetch(query)
        return result

# Define your routes here
@app.post("/insert_data")
async def insert_data(data: dict = Body(pokemons_list)):
    async with app.state.db.acquire() as connection:
        
        try:
            query = "INSERT INTO pokemons (name, image, type) VALUES ($1, $2, $3)"
            # Modify the query and values as needed

            # Execute the query with the provided data
            pokeapi = requests.get('https://pokeapi.co/api/v2/pokemon?limit=2000')
            # data_pokemons = pokemons.text
            # parse_json = json.loads(data_pokemons)
            parse_json = pokeapi.json()
            count = pokeapi.json()['count']
    
            for x in range(1,50):
                pokemon_name = pokeapi.json()['results'][x]['name']
                url = pokeapi.json()['results'][x]['url']
                pokemon_url = requests.get(url)
                pokemon_image = pokemon_url.json()['sprites']['front_default']
                pokemon_type = pokemon_url.json()['types'][0]['type']['name']
                pokemons = {'name': pokemon_name,'image':pokemon_image,'type': pokemon_type}
                await connection.execute(query, pokemon_name, pokemon_image, pokemon_type)
                
            #await connection.execute(query, data['name'], data['image'], data['type'])
            
            return {"message": "Data inserted successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")