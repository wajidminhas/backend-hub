from fastapi import FastAPI
from .router import product

app = FastAPI(title="Imtiaz Mart Product Service")
app.include_router(product.router)