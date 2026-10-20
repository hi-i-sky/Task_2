import requests
import allure
from constants.urls import USER_URL, LOGIN_USER_URL, ORDER_URL, CREATE_USER_URL, INGREDIENTS_URL


def delete_user_by_token(user_access_token):

    headers = {"Authorization": user_access_token}
    r = requests.delete(USER_URL, headers=headers)
    
    return r


def get_user_access_token(email, password):

    payload = {"email": email, "password": password}
    r = requests.post(LOGIN_USER_URL, json=payload)

    assert r.status_code == 200, "Не удалось получить токен пользователя"
    return r.json()['accessToken']



@allure.step('Отправить PATCH-запрос на изменение данных пользователя с авторизацией')
def change_user_data_with_authorization(payload, token):
    return requests.patch(USER_URL, json=payload, headers={'Authorization': token})


@allure.step('Отправить PATCH-запрос на изменение данных пользователя без авторизации')
def change_user_data_without_authorization(payload):
    return requests.patch(USER_URL, json=payload)



@allure.step('Отправить POST-запрос на создание заказа с авторизацией')
def create_order_with_authorization(payload, token):
    return requests.post(ORDER_URL, json=payload, headers={'Authorization': token})


@allure.step('Отправить POST-запрос на создание заказа без авторизации')
def create_order_without_authorization(payload):
    return requests.post(ORDER_URL, json=payload)


@allure.step('Отправить POST-запрос на создание пользователя')
def create_user(payload):
    return requests.post(CREATE_USER_URL, json=payload)


@allure.step('Отправить GET-запрос на получение заказов пользователя с авторизацией')
def get_user_orders_with_authorization(token):
    return requests.get(ORDER_URL, headers={'Authorization': token})


@allure.step('Отправить GET-запрос на получение заказов пользователя без авторизации')
def get_user_orders_without_authorization():
    return requests.get(ORDER_URL)


@allure.step('Отправить POST-запрос на логин пользователя')
def login_user(payload):
    return requests.post(LOGIN_USER_URL, json=payload)


@allure.step('Отправить GET-запрос на получение списка ингредиентов')
def get_ingredients():
    return requests.get(INGREDIENTS_URL)