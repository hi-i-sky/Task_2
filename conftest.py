import pytest
import random
from helpers import delete_user_by_token, get_user_access_token, create_user, get_ingredients, create_order_with_authorization, generate_user_payload


@pytest.fixture
def created_user():
    random_user_payload = generate_user_payload()

    r = create_user(random_user_payload)
    r.raise_for_status()

    data = r.json()

    user_access_token = data['accessToken']
    user_email = data['user']['email']
    user_name = data['user']['name']

    yield {
        'token': user_access_token, 
        'email': user_email, 
        'name': user_name,
        'password': random_user_payload['password']
    }

    delete_user_by_token(user_access_token)


@pytest.fixture
def cleanup_user():
    random_user_payload = generate_user_payload()
    yield random_user_payload

    email = random_user_payload['email']
    password = random_user_payload['password']
    user_access_token = get_user_access_token(email, password)
    delete_user_by_token(user_access_token)


@pytest.fixture
def ingredients_ids():

    r = get_ingredients()
    r.raise_for_status()
    data = r.json()

    ingredients_ids = [item['_id'] for item in data['data']]

    return random.sample(ingredients_ids, 3)


@pytest.fixture
def created_order(created_user, ingredients_ids):

    payload = {'ingredients': ingredients_ids}

    r = create_order_with_authorization(payload, created_user['token'])
    r.raise_for_status()
    response_data = r.json()

    return {
        'order_number': response_data['order']['number'],
        'order_id': response_data['order']['_id'],
        'token': created_user['token'],
        'email': created_user['email'],
    }