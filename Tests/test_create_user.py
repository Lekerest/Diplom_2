import pytest
import requests
import allure
from urls import Urls
from helpers import CourierHelper


class TestCreateUser:

    @allure.title("Создание уникального пользователя")
    @allure.description("Проверка успешного создания нового пользователя с валидными данными.")
    def test_create_unique_user(self, request):
        email = CourierHelper.email_address()
        password = CourierHelper.generate_random_string(10)
        name = CourierHelper.generate_random_string(10)

        payload = {
            "email": email,
            "password": password,
            "name": name
        }

        with allure.step("Отправка POST-запроса на создание пользователя"):
            response_create_user = requests.post(f'{Urls.BASE_URL}{Urls.AUTH_REGISTER}', json=payload)

        request.addfinalizer(lambda: CourierHelper.delete_user(response_create_user))

        with allure.step("Проверка, что статус-код равен 200"):
            assert response_create_user.status_code == 200, \
                f"Ожидался статус 200, но получен {response_create_user.status_code}. Ответ: {response_create_user.text}"

        with allure.step("Проверка тела ответа на успешное создание"):
            body = response_create_user.json()
            assert body["user"]["email"] == email, "Email пользователя не совпадает"
            assert body["user"]["name"] == name, "Имя пользователя не совпадает"

    @allure.title("Создание уже существующего пользователя")
    @allure.description("Проверка, что нельзя создать пользователя с уже зарегистрированным email.")
    def test_create_existing_user(self, register_new_user):
        response, [email, password, name] = register_new_user
        payload = {
            "email": email,
            "password": password,
            "name": name
        }

        with allure.step("Повторная отправка POST-запроса на создание пользователя с теми же данными"):
            response_create_user = requests.post(f'{Urls.BASE_URL}{Urls.AUTH_REGISTER}', json=payload)

        with allure.step("Проверка, что статус-код равен 403"):
            assert response_create_user.status_code == 403, \
                f"Ожидался статус 403, но получен {response_create_user.status_code}. Ответ: {response_create_user.text}"

        with allure.step("Проверка тела ответа на сообщение об уже существующем пользователе"):
            body = response_create_user.json()
            assert body.get("message") == "User already exists", \
                f"Ожидалось сообщение 'User already exists', но получено: {body.get('message')}"

    @allure.title("Создание пользователя с неполными данными")
    @allure.description("Проверка, что создание пользователя невозможно без обязательных полей.")
    @pytest.mark.parametrize(
        "email, password, description",
        [
            ("", CourierHelper.generate_random_string(10), "без email"),
            (CourierHelper.email_address(), "", "без пароля"),
        ]
    )
    def test_create_user_with_missing_fields(self, email, password, description):
        payload = {
            "email": email,
            "password": password,
            "name": CourierHelper.generate_random_string(10)
        }

        with allure.step(f"Отправка POST-запроса на создание пользователя {description}"):
            response = requests.post(f'{Urls.BASE_URL}{Urls.AUTH_REGISTER}', json=payload)

        with allure.step("Проверка, что статус-код равен 403"):
            assert response.status_code == 403, \
                f"Ожидался статус 403, но получен {response.status_code}. Ответ: {response.text}"

        with allure.step("Проверка тела ответа на отсутствие обязательных полей"):
            body = response.json()
            assert body.get("message") == "Email, password and name are required fields", \
                f"Ожидалось сообщение 'Email, password and name are required fields', но получено: {body.get('message')}"
