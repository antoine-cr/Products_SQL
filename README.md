# Products_SQL
Ce projet a pour but la mise en place d'une base de données SQLAlchemy et la création d'une API contenant des produits d'amazon co-ecommerce à l'aide de FastAPI.

## Démarrage API
Se rendre sur le répertoire /api et exécuter la commande docker-compose up (chargement des données + création de l'api)

## Routes:

http://0.0.0.0:8000/products pour lister tous les produits de la bdd (limité à l'affichage)

http://0.0.0.0:8000/products/{uniq_id} pour trouver un produit à partir de son id

http://0.0.0.0:8000/products_name/{product_name} pour trouver un ou des produit(s) à partir de son nom

http://0.0.0.0:8000/products_manufacturer/{manufacturer} pour trouver un ou des produit(s) à partir d'un fabricant

http://0.0.0.0:8000/products_rating/{average_rating} pour trouver un ou des produit(s) à une note moyenne recherchée

http://0.0.0.0:8000/products_price/{price} pour trouver un ou des produit(s) à un prix recherché

