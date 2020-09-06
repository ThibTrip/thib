"""
Simple example app for the "fastapi" library.

Resources:
* https://fastapi.tiangolo.com/ (main page of fastapi's library)

Usage:
$ pip install uvicorn
* during development
$ uvicorn simple_fastapi:app --reload
* deploying
$ uvicorn simple_fastapi:app --host 0.0.0.0 --port 80
"""
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel


# # JSON Models for the API

class Product(BaseModel):
    # fast API will read the typing and convert
    # python types for the API automatically
    name: str
    price_per_unit: float
    quantity: int
    attributes : dict


# # Create the API

# +
app = FastAPI()

@app.get("/")
def read_root(name: Optional[str]="world"):
    """
    Greets a user of the API.
    """
    return f"Hello {name}"

@app.post("/catalog/add")
def add_item(product: Product):
    """
    Pretends to add a product to an online catalog somewhere.
    """
    # add some complex logic here (e.g. add the product to a database)
    # see sql_fastapi.py for an example with a database

    # here we will just send a message pretending we added the product
    return f'A product has been added: {product.dict()}'
