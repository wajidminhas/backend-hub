
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import EmailStr, BaseModel

app = FastAPI()


def write_notification(email :EmailStr, message: str ="" ):
    with open("log.txt", mode = "w") as email_file:
        content = f"Email: {email}\nMessage: {message}"
        email_file.write(content)

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


# app = FastAPI()


# @app.post("/items/")
async def create_item(item: Item):
    try:
        if item in Item:
            return item
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
    

# @app.get('/items/{item_id}')
async def read_item(item_id : str , q : str | None = None):
    if q:
        return{"item_id" : item_id, "q" : q}
    return {"item_id" : item_id}

    
# @app.get('/items/{item_id}')
async def read_item(item_id : str, q : str | None = None, short : bool = False):
    item = {"item" : item_id}
    if q :
        item.update({"q" : q})
    if not short :
        item.update({"Message" : "this is a long description mesaage"})
    return item

# @app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item