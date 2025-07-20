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

    @allure.title("Создание пользователя без email")
    @allure.description("Проверка, что создание пользователя без email невозможно.")
    def test_create_user_without_login(self):
        payload = {
            "email": "",
            "password": CourierHelper.generate_random_string(10),
            "name": CourierHelper.generate_random_string(10)
        }

        with allure.step("Отправка POST-запроса на создание пользователя без email"):
            response_create_user = requests.post(f'{Urls.BASE_URL}{Urls.AUTH_REGISTER}', json=payload)

        with allure.step("Проверка, что статус-код равен 403"):
            assert response_create_user.status_code == 403, \
                f"Ожидался статус 403, но получен {response_create_user.status_code}. Ответ: {response_create_user.text}"

    @allure.title("Создание пользователя без пароля")
    @allure.description("Проверка, что создание пользователя без пароля невозможно.")
    def test_create_user_without_password(self):
        payload = {
            "email": CourierHelper.email_address(),
            "password": "",
            "name": CourierHelper.generate_random_string(10)
        }

        with allure.step("Отправка POST-запроса на создание пользователя без пароля"):
            response_create_user = requests.post(f'{Urls.BASE_URL}{Urls.AUTH_REGISTER}', json=payload)

        with allure.step("Проверка, что статус-код равен 403"):
            assert response_create_user.status_code == 403, \
                f"Ожидался статус 403, но получен {response_create_user.status_code}. Ответ: {response_create_user.text}"
