from fastapi import FastAPI, HTTPException
from modles import Item
app = FastAPI()



# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     if item_id < 0:
#         raise HTTPException(status_code=400, detail="Item ID must be a positive integer")
#     return {"item_id": item_id}

# @app.post("/items")
# async def create_item(item: Item):
#     return item

# @app.get("/users/{user_id}")
# async def read_user(user_id: str):
#     return {"user_id": user_id}

@app.get("/users")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@app.get("/users")
async def read_user2():
    return {"username": "john"}


@app.get("/items/")
async def read_items(q: str = None, limit: int = 10):
    return {"query": q, "limit": limit}

@app.post("/items")
async def create_item(item : Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict