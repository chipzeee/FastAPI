from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import session,engine
from models import Products
import database_models
from sqlalchemy.orm import Session

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://192.168.0.122:3000"],
    allow_methods=['*']
)

#Let create one table
database_models.Base.metadata.create_all(bind=engine)

@app.get('/')
def greet():
    return "Hello boss"

products=[
    Products(id=1,name="pen",price=10,quantity=100),
    Products(id=2,name="Bags",price=400,quantity=1)
]

#adding the products of non-alchemy class to the database

# def init():
#     db=session()
#     count=db.query(database_models.Products).count
#     if count!=0:
#         return
#     for product in products:

#         db.add(database_models.Products(**product.model_dump()))
#     db.commit()
# init()

#Creating db injection

def get_db():
    
    db=session()
    try:
        yield db
    finally:
        db.close()


@app.get('/products')


def get_all_products(db: Session=Depends(get_db)):
    #create session
    # db=session()

    db_products=db.query(database_models.Products).all()
    
    return db_products

@app.get('/products/{id}')
def get_product_by_id(id : int, db: Session=Depends(get_db)):

    # for product in products:
    #     if product.id==id:
    #         return product
    # return "Product not found!!"

    db_product=db.query(database_models.Products).filter(database_models.Products.id==id).first()
    if db_product:
        return db_product
    return "Product Not Found!!"


@app.post('/products')
def add_product(product:Products,db : Session=Depends(get_db)):
    # products.append(product)
    # return f"Product added. {product}"
    db.add(database_models.Products(**product.model_dump()))
    db.commit()
    return "Product added"   
 

@app.put('/products/{id}')
def update_product(id:int,product:Products, db: Session=Depends(get_db)):

    # for i in range(len(products)):
    #     if products[i].id==id:
    #         products[i]=product
    #         return "Product updated successfully!"
    # return "Product with given id not found!!"
    db_product=db.query(database_models.Products).filter(database_models.Products.id==id).first()
    if db_product:
        db_product.name=product.name
        db_product.price=product.price
        db_product.quantity=product.quantity
        db.commit()
        return "Product updated."
    return "Product Not Found!!!"


@app.delete('/products/{id}')
def delete_product(id:int, db: Session=Depends(get_db)):
    # for product in products:
    #     if product.id==id:
    #         products.remove(product)
    #         return "Product deleted."
    # return "Product not found"
    db_product=db.query(database_models.Products).filter(database_models.Products.id==id).first()
    if db_product:
            db.delete(db_product)
            db.commit()
            return "Product Deleted."
    return "Product Not found."