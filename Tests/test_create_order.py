import requests
import allure
from urls import Urls
from data import OrderTestData


class TestCreateOrderAuthorized:

    @allure.title("Создание заказа c ингредиентами авторизованным пользователем")
    @allure.description(
        "Проверка, что авторизованный пользователь может успешно создать заказ с ингредиентами, "
        "передав токен в заголовке Authorization.")
    def test_create_order_authorized(self, register_new_user):
        response_register, _ = register_new_user
        access_token = response_register.json()["accessToken"]
        payload = {"ingredients": OrderTestData.VALID_INGREDIENTS}
        headers = {"Authorization": access_token}

        with allure.step("Отправка POST-запроса на создание заказа с токеном авторизации"):
            response = requests.post(f"{Urls.BASE_URL}{Urls.ORDERS}", json=payload, headers=headers)

        with allure.step("Проверка, что статус-код равен 200 (успешное создание заказа)"):
            assert response.status_code == 200, f"Ожидался статус 200, но получен {response.status_code}."

        with allure.step("Проверка содержимого тела ответа"):
            body = response.json()
            assert body.get("success") is True, f"Ожидалось 'success: True', но получено: {body}"
            assert "order" in body, "В ответе отсутствует ключ 'order'"
            assert "number" in body["order"], "В заказе отсутствует номер заказа"

    @allure.title("Создание заказа без авторизации")
    @allure.description(
        "Проверка, что при попытке создания заказа без передачи токена авторизации возвращается статус 401.")
    def test_create_order_without_authorization(self):
        payload = {"ingredients": OrderTestData.VALID_INGREDIENTS}

        with allure.step("Отправка POST-запроса на создание заказа без токена авторизации"):
            response = requests.post(f"{Urls.BASE_URL}{Urls.ORDERS}", json=payload)

        with allure.step("Проверка, что статус-код равен 401 (отказ в авторизации)"):
            assert response.status_code == 401, f"Ожидался статус 401, но получен {response.status_code}."

        with allure.step("Проверка содержимого тела ответа"):
            body = response.json()
            assert body.get("success") is False, "Ожидалось 'success: False'"
            assert "message" in body, "Ожидалось наличие поля 'message' в теле ответа"

    @allure.title("Создание заказа с авторизацией без ингредиентов")
    @allure.description(
        "Проверка, что при попытке создания заказа с авторизацией, но без ингредиентов, возвращается статус 400.")
    def test_create_order_without_ingredients(self, register_new_user):
        response_register, _ = register_new_user
        access_token = response_register.json()["accessToken"]
        payload = {"ingredients": OrderTestData.EMPTY_INGREDIENTS}
        headers = {"Authorization": access_token}

        with allure.step("Отправка POST-запроса на создание заказа с пустым списком ингредиентов"):
            response = requests.post(f"{Urls.BASE_URL}{Urls.ORDERS}", json=payload, headers=headers)

        with allure.step("Проверка, что статус-код равен 400 (некорректный запрос)"):
            assert response.status_code == 400, f"Ожидался статус 400, но получен {response.status_code}."

        with allure.step("Проверка содержимого тела ответа"):
            body = response.json()
            assert body.get("success") is False, "Ожидалось 'success: False'"
            assert "message" in body, "Ожидалось наличие поля 'message' в теле ответа"

    @allure.title("Создание заказа с неверным идентификатором ингредиента")
    @allure.description(
        "Проверка, что при передаче некорректного идентификатора ингредиента возвращается статус 500.")
    def test_create_order_with_wrong_ingredient(self, register_new_user):
        response_register, _ = register_new_user
        access_token = response_register.json()["accessToken"]
        fake_ingredient = OrderTestData.INVALID_INGREDIENT
        payload = {"ingredients": fake_ingredient}
        headers = {"Authorization": access_token}

        with allure.step("Отправка POST-запроса на создание заказа с неверным идентификатором ингредиента"):
            response = requests.post(f"{Urls.BASE_URL}{Urls.ORDERS}", json=payload, headers=headers)

        with allure.step("Проверка, что статус-код равен 500 (ошибка сервера)"):
            assert response.status_code == 500, f"Ожидался статус 500, но получен {response.status_code}."

        with allure.step("Проверка, что тело ответа является html"):
            assert "<html" in response.text.lower(), "Ожидался HTML в теле ответа при ошибке 500, но получено что-то другое"
