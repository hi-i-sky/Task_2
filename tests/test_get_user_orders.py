import requests
import allure
from constants.urls import ORDER_URL
from constants.errors_texts import ERROR_401_WHEN_GETTING_USER_ORDERS_WITHOUT_AUTORIZATION


class TestGetUserOrders:

    @allure.title('Проверка ручки /api/orders: успешное получение заказа пользователя')
    def test_get_user_orders_with_autorization_success(self, created_user, created_order):

        r = requests.get(ORDER_URL, headers={"Authorization": created_user['token']})

        orders = r.json()["orders"]
        
        assert r.status_code == 200
        assert len(orders) == 1
        assert orders[0]['_id'] == created_order['order_id']


    @allure.title('Проверка ручки /api/orders: ошибка 401 при попытке получить заказ пользователя не авторизовавшись')
    def test_get_user_orders_without_autorization_error(self, created_user, created_order):

        r = requests.get(ORDER_URL)

        assert r.status_code == 401
        assert r.json()['message'] == ERROR_401_WHEN_GETTING_USER_ORDERS_WITHOUT_AUTORIZATION