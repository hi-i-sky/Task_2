import requests
from constants.urls import USER_URL, LOGIN_USER_URL


def delete_user_by_token(user_access_token):

    headers = {"Authorization": user_access_token}
    r = requests.delete(USER_URL, headers=headers)
    
    return r


def get_user_access_token(email, password):

    payload = {"email": email, "password": password}
    r = requests.post(LOGIN_USER_URL, json=payload)

    assert r.status_code == 200, "Не удалось получить токен пользователя"
    return r.json()['accessToken']