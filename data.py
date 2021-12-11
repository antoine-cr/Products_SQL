import pandas as pd

#Récupération de la BDD dans un dataframe
df = pd.read_csv('https://query.data.world/s/dg5twy2l5jlhlrn6xrookyrfla6ddd')

#Simplification de la variable de notation
df['average_rating']=df['average_review_rating'].str.split(' ').str[0]
df['average_rating']=df['average_rating'].astype(float)

#Nettoyage de la variable du nombre de reviews
df['number_of_reviews']=df['number_of_reviews'].fillna('0')
df['number_of_reviews']=df['number_of_reviews'].replace(',','', regex=True)
df['number_of_reviews']=df['number_of_reviews'].astype(int)


df['number_of_answered_questions']=df['number_of_answered_questions'].fillna('0')
df['number_of_answered_questions']=df['number_of_answered_questions'].astype(int)

#Simplification de la variable price
df['price']=df['price'].replace('£','', regex=True)
df['price']=df['price'].replace(',','', regex=True)
df['price']=df['price'].str.split(' ').str[0]
df['price']=df['price'].astype(float)

#Création d'un nouveau dataframe ne contenant que des variables pertinentes pour la recherche
data = df[['uniq_id','product_name','amazon_category_and_sub_category', 'manufacturer','price','number_available_in_stock','number_of_reviews','number_of_answered_questions','average_rating']].copy()

data.to_csv('./amazon_co-ecommerce_sample.csv', header=False, index=False)

