from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base

class Pokemons(Base):
    __tablename__ = "pokemons"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    image = Column(String, nullable=False)
    type = Column(String, nullable=False)
    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
