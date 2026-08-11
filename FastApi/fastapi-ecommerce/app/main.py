



from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class Item(BaseModel):
    name : str
    price : float
    is_offer : bool | None = None
    
class Person(BaseModel):
    f_name : str
    l_name : str


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item : str, item_id : int):
    return {"item" : item, "item_id" : item_id}


@app.post("/personal-info")
async def get_personal_detail(personal_data : Person):
    
    return {"person_f_name" : personal_data.f_name, "persone_l_name" : personal_data.l_name}

@app.put("/item/{item_id}")
async def update_item(item_id : str, item : Item):
    return {"item_name" : item.name, "item_price" : item.price, "item_id" : item_id}

