import pytest
import allure
from constants.errors_texts import ERROR_401_WHEN_LOGIN_USER_WITHOUT_REQUIRED_FIELD
from helpers import login_user, generate_user_payload


class TestLoginUser:

    @allure.title('Проверка ручки /api/auth/login: успешный логин пользователя')
    def test_login_correct_credentials_success(self, created_user):

        payload = {
            "email": created_user["email"],
            "password": created_user["password"],
        }

        r = login_user(payload)

        data = r.json()

        assert r.status_code == 200
        assert 'user' in data
        assert 'accessToken' in data
        assert 'refreshToken' in data


    @allure.title('Проверка ручки /api/auth/login: ошибка 401 при попытке логина пользователя без одного из двух обязательных полей')
    @pytest.mark.parametrize('field', ['email', 'password'])
    def test_login_without_required_field_error(self, field):

        payload = {k: v for k, v in generate_user_payload().items() if k == field}

        r = login_user(payload)

        assert r.status_code == 401
        assert r.json()['message'] == ERROR_401_WHEN_LOGIN_USER_WITHOUT_REQUIRED_FIELD