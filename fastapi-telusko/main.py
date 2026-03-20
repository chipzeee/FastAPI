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