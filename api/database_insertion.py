from numpy import genfromtxt
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
import argparse
import subprocess
import os
import sys
import pandas as pd

sys.stdout = open('log.txt')

def Load_Data(file_name):
    data = genfromtxt(file_name, delimiter=';', skip_header=1, converters={0: lambda s: str(s)})
    return data.tolist()

Base = declarative_base()

#Création de la table product
class Product(Base):
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

if __name__ == "__main__":

    #Création de la BDD
    engine = create_engine('sqlite:///products.db')
    Base.metadata.create_all(engine)

    #Création de la session
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    with open("amazon_co-ecommerce_sample.csv", 'r') as file:
        data_df = pd.read_csv(file, delimiter=";")
        data_df.to_sql('product', con=engine, index=True, index_label='id', if_exists='replace')
