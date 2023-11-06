from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

import requests
import asyncio
import asyncpg
import time

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         # with psycopg.connect("host=localhost database=fastapi user=postgres password=pukar123#") as conn:
#         conn = psycopg2.connect(host='localhost', dbname='fastapi', user='postgres',
#                                 password='pukar123#',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
        
#         print("Database connection was succesfull!")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)



# async def run():
#     # Establish a connection to an existing database named "test"
#     # as a "postgres" user.
#     pokeapi = requests.get('https://pokeapi.co/api/v2/pokemon?limit=2000')
#     pokemons_list = []
#     parse_json = pokeapi.json()
#     count = pokeapi.json()['count']
    
#     for x in range(1,5):
#         pokemon_name = pokeapi.json()['results'][x]['name']
#         url = pokeapi.json()['results'][x]['url']
#         pokemon_url = requests.get(url)
#         pokemon_image = pokemon_url.json()['sprites']['front_default']
#         pokemon_type = pokemon_url.json()['types'][0]['type']['name']
#         pokemons = {'name': pokemon_name,'image':pokemon_image,'type': pokemon_type}
#         pokemons_list.append(pokemons)
#     print(pokemons_list)

#     conn = await asyncpg.connect('postgresql://postgres:pukar123#@localhost/fastapi')

#     # Insert a record into the created table.
#     # await conn.execute('''
#     #     INSERT INTO users(name, dob) VALUES($1, $2)
#     # ''', 'Bob', datetime.date(1984, 3, 1))

#     # Close the connection.
#     values = await conn.fetch('SELECT * FROM users WHERE id = 1',10,)

#     await conn.close()

# loop = asyncio.get_event_loop()
# loop.run_until_complete(run())