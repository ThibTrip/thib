# -*- coding: utf-8 -*-
# +
"""
Example app with SQL for the "fastapi" library.

The tutorial for SQL databases on FAST API is long and complex which is why we use
the library "fastapi_sqlalchemy" which reduces boilerplate.

It's still probably good to go quickly over the tutorial on fastapi to get an idea
of how it works.

Resources:
* https://fastapi.tiangolo.com/ (main page of fastapi's library)
* https://fastapi.tiangolo.com/tutorial/sql-databases/ (tutorial for SQL on fastapi)
* https://github.com/mfreeborn/fastapi-sqlalchemy/

Usage:
$ pip install uvicorn
* during development
$ uvicorn sql_fastapi:app --reload
* deploying
$ uvicorn sql_fastapi:app --host 0.0.0.0 --port 80
"""
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware  # middleware helper
from fastapi_sqlalchemy import db  # an object to provide global access to a database session
from pydantic import BaseModel
from loguru import logger # awesome logging library, I highly recommand using it
logger.add("sql_fastapi.log", rotation="1 day") # add logging to file, rotate every day

from sqlalchemy import Boolean, Column, Float, Integer, String, JSON
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
# -

# # Create a catalog table

# +
engine = create_engine("postgresql+psycopg2://postgres:password@localhost:5432/postgres")
Base = declarative_base()

class Catalog(Base):
    __tablename__ = "catalog"
    __table_args__ = {'schema':'tests'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    price_per_unit = Column(Float)
    quantity = Column(Integer)
    attributes = Column(JSON)

# creates table Catalog (with the columns defined above) if it does not exist
Base.metadata.create_all(bind=engine)


# -

# # JSON Models for the API

class Product(BaseModel):
    # fast API will read the typing and convert
    # python types for the API automatically
    name: str
    price_per_unit: float
    quantity: int
    attributes : dict


# # Create the API
#
# Note: you cannot use numpy's docstring style, you have to use a specific syntax as we do below in the function get_product (the syntax seems to be Markdown). See https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#description-from-docstring

# +
app = FastAPI()

# once the middleware is applied, any route can then access the database session from the global ``db``
app.add_middleware(DBSessionMiddleware,
                   db_url="postgresql+psycopg2://postgres:password@localhost:5432/postgres",
                   # there is no docstring but this seems to commits each time a session is terminated
                   # if this was False (default) then db.sesions.add(item) would not do anything
                   commit_on_exit=True)

@app.post("/catalog/add")
def add_product(product:Product):
    """
    Adds a product to a "catalog" table in our PostgreSQL database.
    """
    # add a row inside the "catalog" table
    item = Catalog(**product.dict()) # e.g. Catalog(name='banana', price_per_unit=0.5, ...)
    db.session.add(item)

    # maybe we want to do some logging
    logger.info(f'Product "{product.name}" added')

    # tell the user it worked
    return f'The product "{product.name}" has been successfully added 🐵!'

@app.get("/catalog/{name}")
def get_product(name:str):
    """
    Gets information on a product using its name.

    ## Parameters

    - **name**: Name of the product e.g. "banana"
    """
    return db.session.query(Catalog).filter(Catalog.name==name).first()
