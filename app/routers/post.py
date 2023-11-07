from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/api/v1",
    tags=['Posts']
)

@router.get("/pokemons", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Pokemons).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db)):
    new_post = models.Pokemons(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/name/{name}")
def get_post(name: str, response: Response,db: Session = Depends(get_db)):
    post = db.query(models.Pokemons).filter(models.Pokemons.name == name).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post not found with name:{name}")
    return post

@router.get("/type/{type}")
def get_post(type: str, response: Response,db: Session = Depends(get_db)):
    post = db.query(models.Pokemons).filter(models.Pokemons.type == type).all()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post not found with type:{type}")
    return post