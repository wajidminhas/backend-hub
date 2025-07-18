
from fastapi import FastAPI, BackgroundTasks
from pydantic import EmailStr

app = FastAPI()


def write_notification(email :EmailStr, message: str ="" ):
    with open("log.txt", mode = "w") as email_file:
        content = f"Email: {email}\nMessage: {message}"
        email_file.write(content)

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}