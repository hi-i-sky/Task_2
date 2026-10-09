import pytest
from faker import Faker
import requests
from constants.urls import CREATE_USER_URL, USER_URL
from helpers import delete_user_by_token, get_user_access_token



@pytest.fixture
def random_user_payload():
    fake = Faker()
    return {
        "email": fake.email(),
        "password": fake.password(),
        "name": fake.first_name()
    } 


@pytest.fixture
def created_user(random_user_payload):

    r = requests.post(CREATE_USER_URL, json=random_user_payload)
    r.raise_for_status()

    user_access_token = r.json()['accessToken']

    yield user_access_token

    delete_user_by_token(user_access_token)


@pytest.fixture
def cleanup_user(random_user_payload):

    yield random_user_payload

    email = random_user_payload["email"]
    password = random_user_payload["password"]
    user_access_token = get_user_access_token(email, password)
    delete_user_by_token(user_access_token)