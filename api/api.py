from typing import List
from typing import List, Optional
from pydantic import BaseModel, AnyStrMinLengthError, types
from fastapi import FastAPI, Depends, Header, HTTPException, status

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, text, inspect
from sqlalchemy import Column, Integer, String, ForeignKey

from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import concat
from sqlalchemy.sql.sqltypes import ARRAY, FLOAT, VARCHAR, String, Integer
from sqlalchemy.sql.type_api import STRINGTYPE
from sqlalchemy import insert

from model import ProductData

Base = declarative_base()

class Products(Base):
    __tablename__ = "product"
    id = Column(Integer, index=True)
    uniq_id = Column(String, primary_key=True, index=True)
    product_name = Column(String, unique=True, index=True)
    amazon_category_and_sub_category = Column(String)
    manufacturer = Column(String)
    price = Column(String)
    number_available_in_stock = Column(String)
    number_of_reviews = Column(Integer)
    number_of_answered_questions= Column(Integer)
    average_rating = Column(String)

#Création de la BDD
engine = create_engine('sqlite:///products.db', echo=True)
conn = engine.connect()

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
    
# Définition des fonctions
def get_product(db: Session, product_uniq_id: int):
    ''' permet de récupérer l'uniq_id du produit.'''
    return db.query(Products).filter(Products.uniq_id == product_uniq_id).first()

def get_product_name(db: Session, product_product_name: str, limit: int =100):
    ''' permet de récupérer le nom du produit.'''
    return db.query(Products).filter(Products.product_name == product_product_name).limit(limit).all()

def get_product_manufacturer(db: Session, product_manufacturer: str, limit: int =100):
    ''' permet de récupérer le fabricant du produit.'''
    return db.query(Products).filter(Products.manufacturer == product_manufacturer).limit(limit).all()

def get_product_rating(db: Session, product_average_rating: float, limit: int =100):
    ''' permet de récupérer l'évaluation du produit.'''
    return db.query(Products).filter(Products.average_rating == product_average_rating).limit(limit).all()

def get_product_price(db: Session, product_price: float, limit: int =100):
    ''' permet de récupérer le prix du produit.'''
    return db.query(Products).filter(Products.price == product_price).limit(limit).all()

def get_products(db: Session, skip: int = 0, limit: int = 50):
    ''' permet de limiter l'id du produit.'''
    return db.query(Products).offset(skip).limit(limit).all()

def insert_product(db: Session, data: ProductData):
    id_new = int(db.execute("SELECT MAX(id) from product").fetchall()[0][0])+1
    if(db.execute(("SELECT uniq_id from product WHERE uniq_id = '"+data.uniq_id+"'")).fetchall() == []):
        new_Product = Products(id=id_new, uniq_id=data.uniq_id, product_name=data.product_name, amazon_category_and_sub_category=data.amazon_category_and_sub_category, manufacturer=data.manufacturer, price=data.price, number_available_in_stock=data.number_available_in_stock, number_of_reviews=data.number_of_reviews, number_of_answered_questions=data.number_of_answered_questions, average_rating=data.average_rating)
        db.add(new_Product)
        db.commit()
        print(id_new)
    else:
        raise HTTPException(status_code=404, detail="Product already exists with uniq_id")
    return db.query(Products).filter(Products.id == id_new).all()

def delete_product(db: Session, product_product_name: str, limit: int =100):
    del_Product = db.query(Products).filter(Products.product_name == product_product_name).limit(limit).all()
    db.delete(del_Product)
    db.commit()
    return db.query(Products).filter(Products.id == del_Product.id).first()

# Création des routes
@api.get("/products/")
def search_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = get_products(db, skip=skip, limit=limit)
    return products

@api.get("/products/{uniq_id}")
def search_product(uniq_id: str, db: Session = Depends(get_db)):
    product = get_product(db, product_uniq_id=uniq_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@api.get("/products_name/{product_name}")
def search_product_name(product_name: str, db: Session = Depends(get_db)):
    product = get_product_name(db, product_product_name=product_name)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@api.get("/products_manufacturer/{manufacturer}")
def search_product_manufacturer(manufacturer: str, db: Session = Depends(get_db)):
    product = get_product_manufacturer(db, product_manufacturer=manufacturer)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@api.get("/products_rating/{average_rating}")
def search_product_rating(average_rating: float, db: Session = Depends(get_db)):
    product = get_product_rating(db, product_average_rating=average_rating)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@api.get("/products_price/{price}")
def search_product_price(price: float, db: Session = Depends(get_db)):
    product = get_product_price(db, product_price=price)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@api.post("/products")
def create_product(data: ProductData, db: Session = Depends(get_db)):
    product = insert_product(db, data)
    return product
