from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas
from ..database import get_db

# import requests
# import json

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# pokemons_list = []

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Pokemons).all()
    return posts

# @router.get("/pokemons")
# def get_posts():
#     pokeapi = requests.get('https://pokeapi.co/api/v2/pokemon?limit=2000')
#     # data_pokemons = pokemons.text
#     # parse_json = json.loads(data_pokemons)
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
#     return pokemons_list

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()

    # conn.commit()
    
    new_post = models.Pokemons(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# @router.post("/pokemons/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(post: dict, db: Session = Depends(get_db)):
#     # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
#     #                (post.title, post.content, post.published))
#     # new_post = cursor.fetchone()

#     # conn.commit()
#     print(pokemons_list)
#     print(post)
#     new_post = models.Pokemons(pokemons_list)
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return {"data": "new_post"}



@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, response: Response,db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Pokemons).filter(models.Pokemons.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post not found with id:{id}")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message" : f"post not found with id:{id}"}
    return post

@router.get("/name/{name}")
def get_post(name: str, response: Response,db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Pokemons).filter(models.Pokemons.name == name).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post not found with name:{name}")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message" : f"post not found with id:{id}"}
    return post

@router.get("/type/{type}")
def get_post(type: str, response: Response,db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Pokemons).filter(models.Pokemons.type == type).all()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post not found with type:{type}")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message" : f"post not found with id:{id}"}
    return post