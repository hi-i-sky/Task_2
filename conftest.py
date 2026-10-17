import pytest
from faker import Faker
import requests
import random
from constants.urls import CREATE_USER_URL, INGREDIENTS_URL, ORDER_URL
from helpers import delete_user_by_token, get_user_access_token



@pytest.fixture
def random_user_payload():

    fake = Faker()
    return {
        'email': fake.email(),
        'password': fake.password(),
        'name': fake.first_name()
    } 


@pytest.fixture
def created_user(random_user_payload):

    r = requests.post(CREATE_USER_URL, json=random_user_payload)
    r.raise_for_status()

    data = r.json()

    user_access_token = data['accessToken']
    user_email = data['user']['email']
    user_name = data['user']['name']

    yield {
        'token': user_access_token, 
        'email': user_email, 
        'name': user_name
    }

    delete_user_by_token(user_access_token)


@pytest.fixture
def cleanup_user(random_user_payload):

    yield random_user_payload

    email = random_user_payload['email']
    password = random_user_payload['password']
    user_access_token = get_user_access_token(email, password)
    delete_user_by_token(user_access_token)


@pytest.fixture
def ingredients_ids():

    r = requests.get(INGREDIENTS_URL)
    r.raise_for_status()
    data = r.json()

    ingredients_ids = [item['_id'] for item in data['data']]

    yield random.sample(ingredients_ids, 3)


@pytest.fixture
def created_order(created_user, ingredients_ids):

    payload = {'ingredients': ingredients_ids}
    headers = {'Authorization': created_user['token']}

    r = requests.post(ORDER_URL, json=payload, headers=headers)
    r.raise_for_status()
    response_data = r.json()

    yield {
        'order_number': r.json()['order']['number'],
        'order_id': r.json()['order']['_id'],
        'token': created_user['token'],
        'email': created_user['email'],
    }