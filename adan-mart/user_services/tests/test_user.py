from http import client
import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel
from app.main import app
from app.models import Users
from app.router.user import hashed_password, create_access_token, get_session
from datetime import timedelta


client = TestClient(app)

def test_greet():
    response = client.get("/?name=Adan")
    assert response.status_code == 200
    assert response.json() == "hello Adan! Welcome to Adan Mart"




