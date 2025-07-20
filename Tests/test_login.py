import requests
import allure
from helpers import CourierHelper
from urls import Urls


class TestLogin:

    @allure.title("Авторизация существующего пользователя")
    @allure.description("Проверка успешной авторизации ранее зарегистрированного пользователя по email и паролю.")
    def test_authorization_existing_user(self, register_new_user):
        _, [email, password, _] = register_new_user
        payload = {
            "email": email,
            "password": password
        }
        with allure.step("Отправка POST-запроса на авторизацию с валидными учетными данными"):
            response = requests.post(f"{Urls.BASE_URL}{Urls.AUTH_LOGIN}", json=payload)

        with allure.step("Проверка, что статус-код равен 200"):
            assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}. "

    @allure.title("Авторизация с некорректными данными")
    @allure.description("Проверка, что при вводе случайных email и пароля система возвращает ошибку авторизации.")
    def test_authorization_with_incorrect_data(self):
        payload = {
            "email": CourierHelper.generate_random_string(10),
            "password": CourierHelper.generate_random_string(10)
        }
        with allure.step("Отправка POST-запроса на авторизацию с невалидными учетными данными"):
            response = requests.post(f"{Urls.BASE_URL}{Urls.AUTH_LOGIN}", json=payload)

        with allure.step("Проверка, что статус-код равен 401"):
            assert response.status_code == 401, f"Ожидался статус 401 при неверных данных, но получен {response.status_code}. "
