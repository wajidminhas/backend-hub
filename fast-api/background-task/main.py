from fastapi import FastAPI, BackgroundTasks, Query
from pydantic import EmailStr

app: FastAPI = FastAPI()


@app.get('/')
async def root():
    return {"message": "Welcome to the Notification Service!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id, "message": "This is your item!"}

# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}


async def write_notification(email : EmailStr, message : str = 'You have a new notification!'):
    print(f"Notification sent to {email}: {message}")
    with open('log.txt', mode= "w") as email_file:
        email_file.write(f"{email}\n{message}\n")

@app.post("/send-notification/{email}")
async def send_notification(email: EmailStr, background_tasks: BackgroundTasks):
    """
    Endpoint to send a notification to a user.
    """
    background_tasks.add_task(write_notification, email)
    return {"message": "Notification sent in the background!"}