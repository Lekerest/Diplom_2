import requests
import allure
from helpers import CourierHelper
from urls import Urls


class TestLogin:

    @allure.title("Авторизация существующего пользователя")
    @allure.description("Проверка успешной авторизации ранее зарегистрированного пользователя по email и паролю.")
    def test_authorization_existing_user(self, request):
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

        with allure.step("Отправка POST-запроса на авторизацию с валидными учетными данными"):
            response_login = requests.post(f"{Urls.BASE_URL}{Urls.AUTH_LOGIN}", json=payload)

        with allure.step("Проверка, что статус-код равен 200"):
            assert response_login.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}. "

        with allure.step("Проверка тела ответа на успешное создание"):
            body = response_create_user.json()
            assert body["user"]["email"] == email, "Email пользователя не совпадает"
            assert body["user"]["name"] == name, "Имя пользователя не совпадает"

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

        with allure.step("Проверка тела ответа"):
            body = response.json()
            assert body.get("message") == "email or password are incorrect" \
                f"Ожидалось сообщение 'email or password are incorrect', но получено: {body.get('message')}"