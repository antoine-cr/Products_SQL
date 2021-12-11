from numpy import genfromtxt
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def Load_Data(file_name):
    data = genfromtxt(file_name, delimiter=';', skip_header=1, converters={0: lambda s: str(s)})
    return data.tolist()

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

if __name__ == "__main__":

    #Create the database
    engine = create_engine('sqlite:///products.db')
    Base.metadata.create_all(engine)

    #Create the session
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    try:
        file_name = "/files/amazon_co-ecommerce_sample.csv"
        data = Load_Data(file_name)

        for i in data:
            record = Products(**{
                'uniq_id' : i[0],
                'product_name' : i[1],
                'amazon_category_and_sub_category' : i[2],
                'manufacturer' : i[3],
                'price' : i[4],
                'number_available_in_stock' : i[5],
                'number_of_reviews' : i[6],
                'number_of_answered_questions' : i[7],
                'average_rating' : i[8]
            })
            s.add(record)

        s.commit()
    except:
        s.rollback()
    finally:
        s.close()