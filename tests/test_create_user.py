import pytest
import allure
from constants.errors_texts import ERROR_403_WHEN_CREATING_NOT_NEW_USER, ERROR_403_WHEN_CREATING_USER_WITHOUT_REQUIRED_FIELD
from helpers import create_user


class TestCreateUser:

    @allure.title('Проверка ручки /api/auth/register: успешное создание нового пользователя')
    def test_create_new_user_correct_credentials_success(self, random_user_payload, cleanup_user):

        r = create_user(random_user_payload)

        data = r.json()

        assert r.status_code == 200
        assert 'user' in data
        assert 'accessToken' in data
        assert 'refreshToken' in data


    @allure.title('Проверка ручки /api/auth/register: ошибка 403 при попытке создать уже существующего пользователя')
    def test_create_not_new_user_correct_credentials_error(self, random_user_payload, created_user):

        r = create_user(random_user_payload)

        assert r.status_code == 403
        assert r.json()['message'] == ERROR_403_WHEN_CREATING_NOT_NEW_USER


    @allure.title('Проверка ручки /api/auth/register: ошибка 403 при попытке создать пользователя без одного из трех обязательных полей')
    @pytest.mark.parametrize('field', ['email', 'password', 'name'])
    def test_create_new_user_without_required_field_error(self, random_user_payload, field):

        payload = {k: v for k, v in random_user_payload.items() if k != field}

        r = create_user(payload)

        assert r.status_code == 403
        assert r.json()['message'] == ERROR_403_WHEN_CREATING_USER_WITHOUT_REQUIRED_FIELD