import requests
import allure
from constants.urls import ORDER_URL
from constants.errors_texts import ERROR_400_WHEN_CREATING_ORDER_WITHOUT_INGREDIENTS
from constants.data_sets import INVALID_INGREDIENT_HASH


class TestCreateOrder:

    @allure.title('Проверка ручки /api/orders: успешное создание заказа из 3х ингредиентов с авторизацией')
    def test_create_order_with_authorization_and_ingredients_success(self, created_user, ingredients_ids):

        payload = {'ingredients': ingredients_ids}
        r = requests.post(ORDER_URL, json=payload, headers={'Authorization': created_user['token']})

        data = r.json()
        received_ingredients = data["order"]["ingredients"]
        received_ids = {item["_id"] for item in received_ingredients}

        assert r.status_code == 200
        assert 'number' in data['order']
        assert 'price' in data['order']
        assert received_ids == set(ingredients_ids)
        assert created_user['email'] == data['order']['owner']['email']


    @allure.title('Проверка ручки /api/orders: успешное создание заказа из 3х ингредиентов без авторизации')
    def test_create_order_without_authorization_and_with_ingredients_success(self, ingredients_ids):

        payload = {'ingredients': ingredients_ids}
        r = requests.post(ORDER_URL, json=payload)

        assert r.status_code == 200
        assert 'number' in r.json()['order']


    @allure.title('Проверка ручки /api/orders: ошибка 400 при попытке создать заказ без ингредиентов')
    def test_create_order_without_ingredients_error(self, created_user):

        payload = {'ingredients': None}
        r = requests.post(ORDER_URL, json=payload, headers={'Authorization': created_user['token']})

        assert r.status_code == 400
        assert r.json()['message'] == ERROR_400_WHEN_CREATING_ORDER_WITHOUT_INGREDIENTS


    @allure.title('Проверка ручки /api/orders: ошибка 500 при попытке создать заказ с неверным хешем ингредиента')
    def test_create_order_with_invalid_ingredient_hash_error(self, created_user):

        payload = {'ingredients': [INVALID_INGREDIENT_HASH]}
        r = requests.post(ORDER_URL, json=payload, headers={'Authorization': created_user['token']})

        assert r.status_code == 500

