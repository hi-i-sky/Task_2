import requests
import pytest
import allure
from constants.urls import LOGIN_USER_URL
from constants.errors_texts import ERROR_401_WHEN_LOGIN_USER_WITHOUT_REQUIRED_FIELD


class TestLoginUser:

    @allure.title('Проверка ручки /api/auth/login: успешный логин пользователя')
    def test_login_correct_credentials_success(self, created_user, random_user_payload):

        payload = {
            "email": random_user_payload["email"],
            "password": random_user_payload["password"],
        }

        r = requests.post(LOGIN_USER_URL, json=payload)

        data = r.json()

        assert r.status_code == 200
        assert 'user' in data
        assert 'accessToken' in data
        assert 'refreshToken' in data


    @allure.title('Проверка ручки /api/auth/login: ошибка 401 при попытке логина пользователя без одного из двух обязательных полей')
    @pytest.mark.parametrize('field', ['email', 'password'])
    def test_login_without_required_field_error(self, random_user_payload, field):

        payload = {k: v for k, v in random_user_payload.items() if k == field}

        r = requests.post(LOGIN_USER_URL, json=payload)

        assert r.status_code == 401
        assert r.json()['message'] == ERROR_401_WHEN_LOGIN_USER_WITHOUT_REQUIRED_FIELD