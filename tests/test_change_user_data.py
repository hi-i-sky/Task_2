import pytest
import allure
from constants.errors_texts import ERROR_401_WHEN_CHANGE_USER_DATA_WITHOUT_AUTHORIZATION
from constants.data_sets import CHANGED_EMAIL, CHANGED_NAME, CHANGED_PASSWORD
from helpers import change_user_data_with_authorization, change_user_data_without_authorization


class TestChangeUserData:


    @allure.title('Проверка ручки /api/auth/user: успешное изменение имени и почты пользователя')
    @pytest.mark.parametrize(
        'field, field_value', 
        [
            ['name', CHANGED_NAME],
            ['email', CHANGED_EMAIL]
        ]
    )
    def test_change_user_name_or_email_with_authorization_success(self, created_user, field, field_value):

        payload = {field: field_value}
        r = change_user_data_with_authorization(payload, created_user['token'])

        assert r.status_code == 200
        assert r.json()['user'][field] == field_value


    @allure.title('Проверка ручки /api/auth/user: ошибка 401 при попытке изменить имя и почту пользователя не авторизовавшись')
    @pytest.mark.parametrize(
        'field, field_value', 
        [
            ['name', CHANGED_NAME],
            ['email', CHANGED_EMAIL]
        ]
    )
    def test_change_user_name_or_email_without_authorization_success(self, created_user, field, field_value):

        payload = {field: field_value}
        r = change_user_data_without_authorization(payload)

        assert r.status_code == 401
        assert r.json()['message'] == ERROR_401_WHEN_CHANGE_USER_DATA_WITHOUT_AUTHORIZATION


    @allure.title('Проверка ручки /api/auth/user: успешное изменение пароля пользователя')
    def test_change_user_password_with_authorization_success(self, created_user):

        payload = {'password': CHANGED_PASSWORD}
        r = change_user_data_with_authorization(payload, created_user['token'])

        assert r.status_code == 200
        assert 'user' in r.json()


    @allure.title('Проверка ручки /api/auth/user: ошибка 401 при попытке изменить пароль пользователя не авторизовавшись')
    def test_change_user_password_without_authorization_success(self, created_user):

        payload = {'password': CHANGED_PASSWORD}
        r = change_user_data_without_authorization(payload)

        assert r.status_code == 401
        assert r.json()['message'] == ERROR_401_WHEN_CHANGE_USER_DATA_WITHOUT_AUTHORIZATION