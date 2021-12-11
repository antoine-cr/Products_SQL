from typing import List
from typing import List, Optional
from pydantic import BaseModel
from fastapi import FastAPI, Depends, Header, HTTPException, status

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, text, inspect
from sqlalchemy import Column, Integer, String, ForeignKey

from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

Base = declarative_base()

class Products(Base):
    __tablename__ = "products"

    uniq_id = Column(String, primary_key=True, index=True)
    product_name = Column(String, unique=True, index=True)
    amazon_category_and_sub_category = Column(String)
    manufacturer = Column(Integer)
    price = Column(String)
    number_available_in_stock = Column(String)
    number_of_reviews = Column(Integer)
    number_of_answered_questions= Column(Integer)
    average_rating = Column(String)

#Création de la BDD
engine = create_engine('sqlite:///products.db', echo=True)
conn = engine.connect()

# Test
#stmt = text ( "SELECT * from products limit 5;" )
#result = conn.execute(stmt)
#print(result.fetchall())

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

api = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

security = HTTPBasic()


def get_product(db: Session, product_uniq_id: int):
    return db.query(Products).filter(Products.uniq_id == product_uniq_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 50):
    return db.query(Products).offset(skip).limit(limit).all()

@api.get("/products/")
def search_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = get_products(db, skip=skip, limit=limit)
    return products

@api.get("/products/{uniq_id}")
def search_product(uniq_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_uniq_id=uniq_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
