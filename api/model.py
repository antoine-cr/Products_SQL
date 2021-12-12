# Imporatation des librairies
from pydantic import BaseModel, BaseConfig
from typing import List
from enum import Enum
#from model import pylance


class Product(BaseModel):
    ''' cette classe permet de définir le format des données à envoyer à la requete '''
    uniq_id : str
    product_name : str
    amazon_category_and_sub_category : str
    manufacturer : str
    price : str
    number_available_in_stock : str
    number_of_reviews : int
    number_of_answered_questions : int
    average_rating : str

    class Config(BaseConfig):
        extra = "forbid"

# On recoit les données
ProductData = Product
