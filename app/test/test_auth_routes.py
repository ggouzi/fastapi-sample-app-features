from fastapi.testclient import TestClient
from db import database
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import settings
import pytest
from schemas import token_schema


engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    pool_recycle=21600
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


client = TestClient(app)


@pytest.fixture()
def test_db():
    database.Base.metadata.create_all(bind=engine)
    yield
    database.Base.metadata.drop_all(bind=engine)


def test_login():

    headers = {
        'Content-Type': 'application/json',
        'x-version': '1.0'
    }

    payload = {
        "username": "admin",
        "password": "admin"
    }

    response = client.post("/auth/token", headers=headers, json=payload)
    # Check response code is the expected one
    assert response.status_code == 200
    # Check the response format is the expected one
    assert response.json()
    # Check the response data can be serialized into the expected model
    auth_data = token_schema.AuthToken(**response.json())
    response_dict = response.json()
    assert auth_data.__dict__ == response_dict


def test_outdated_version():

    headers = {
        'Content-Type': 'application/json',
        'x-version': '0.9'
    }

    payload = {
        "username": "admin",
        "password": "admin"
    }

    response = client.post("/auth/token", headers=headers, json=payload)
    # Check response code is the expected one
    assert response.status_code == 426
    # Check the response format is the expected one
    assert response.json()
