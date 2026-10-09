import requests
import pytest
import allure
from constants.urls import USER_URL
from constants.errors_texts import ERROR_401_WHEN_CHANGE_USER_DATA_WITHOUT_AUTHORIZATION
from constants.data_sets import CHANGED_EMAIL, CHANGED_NAME, CHANGED_PASSWORD


class TestChangeUserData:

    @pytest.mark.parametrize(
        'field, field_value', 
        [
            ['name', CHANGED_NAME],
            ['email', CHANGED_EMAIL]
        ]
    )
    def test_change_user_name_or_email_with_authorization_success(self, created_user, field, field_value):

        payload = {field: field_value}
        r = requests.patch(USER_URL, json=payload, headers={'Authorization': created_user})

        assert r.status_code == 200
        assert r.json()['user'][field] == field_value


    @pytest.mark.parametrize(
        'field, field_value', 
        [
            ['name', CHANGED_NAME],
            ['email', CHANGED_EMAIL]
        ]
    )
    def test_change_user_name_or_email_without_authorization_success(self, created_user, field, field_value):

        payload = {field: field_value}
        r = requests.patch(USER_URL, json=payload)

        assert r.status_code == 401
        assert r.json()['message'] == ERROR_401_WHEN_CHANGE_USER_DATA_WITHOUT_AUTHORIZATION


    def test_change_user_password_with_authorization_success(self, created_user):

        payload = {'password': CHANGED_PASSWORD}
        r = requests.patch(USER_URL, json=payload, headers={'Authorization': created_user})

        assert r.status_code == 200
        assert 'user' in r.json()


    def test_change_user_password_without_authorization_success(self, created_user):

        payload = {'password': CHANGED_PASSWORD}
        r = requests.patch(USER_URL, json=payload)

        assert r.status_code == 401
        assert r.json()['message'] == ERROR_401_WHEN_CHANGE_USER_DATA_WITHOUT_AUTHORIZATION