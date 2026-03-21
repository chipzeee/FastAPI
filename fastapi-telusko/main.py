from fastapi import FastAPI
from fastapi.responses import HTMLResponse,FileResponse

from models import Products

app=FastAPI()

@app.get('/')
def greet():
    return "Hello boss"

products=[
    Products(id=1,name="pen",price=10,quantity=100),
    Products(id=2,name="Bags",price=400,quantity=1)
]

@app.get('/products')
def get_all_products():
    return products

@app.get('/products/{id}')
def get_product_by_id(id : int):

    for product in products:
        if product.id==id:
            return product
    return "Product not found!!"

@app.post('/products')
def add_product(product:Products):
    products.append(product)
    return f"Product added. {product}"


@app.put('/products')
def update_product(id:int,product:Products):

    for i in range(len(products)):
        if products[i].id==id:
            products[i]=product
            return "Product updated successfully!"
    return "Product with given id not found!!"


@app.delete('/products')
def delete_product(id:int):
    for product in products:
        if product.id==id:
            products.remove(product)
            return "Product deleted."
    return "Product not found"