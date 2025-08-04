from fastapi import FastAPI, HTTPException, Query , Path, Depends
from typing import Annotated, Optional
from pydantic import BaseModel
from modles import Item, ItemNew, FilterParams
app = FastAPI()


class ItemNew(BaseModel):
    name: str
    price: float
    description: Optional[str] = None


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


# @app.get("/items/")
# async def read_items(q: str = None, limit: int = 10):
#     return {"query": q, "limit": limit}

@app.post("/items")
async def create_item(item : Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# @app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# *********** Path Parameters and Numeric Validations********************/

@app.get("/items/{item_id}")
async def read_items_one(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(
        title="The ID of the item to get",
        description="The ID must be a number greater than 0.",
        ge=1,  # 'ge' stands for "greater than or equal to"
        le=1000 # 'le' stands for "less than or equal to"
    ),
    q: str | None = None
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

@app.put("/items/{item_id}")
async def update_item(
    # 1. Path Parameter (REQUIRED)
    item_id: Annotated[int, Path(ge=1, title="The ID of the item")],

    item_new: ItemNew,
    # 2. Query Parameters (OPTIONAL, with defaults)
    is_active: Annotated[bool, Query(description="Filter by active status")] = True,

    limit: Annotated[int, Query(ge=0, le=100, description="Number of items to return")] = 50

    # 3. Request Body (REQUIRED)
):
    # This ordering is clean and readable for humans
    # FastAPI correctly understands where each parameter comes from
    # because of the explicit `Path`, `Query`, and `Item` (Pydantic model) declarations.

    return {
        "item_id": item_id,
        "limit": limit,
        "is_active": is_active,
        "item": item_new
    }

@app.put("/translations/")
async def get_translations(params: FilterParams = Depends()):
    # Mock database query
    return {
        "translations": [],  # Replace with your agent logic
        "params": params.model_dump()
    }