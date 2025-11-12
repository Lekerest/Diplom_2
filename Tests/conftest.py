import pytest
import requests
import logging
from urls import Urls
from helpers import CourierHelper

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@pytest.fixture
def register_new_user():
    login = CourierHelper.email_address()
    password = CourierHelper.generate_random_string(10)
    name = CourierHelper.generate_random_string(10)

    payload = {
        "email": login,
        "password": password,
        "name": name
    }

    response_create_user = requests.post(f'{Urls.BASE_URL}{Urls.AUTH_REGISTER}', json=payload)

    if response_create_user.status_code == 200:
        logging.info(f"Пользователь создан: login={login}")
    else:
        logging.warning(
            f"Не удалось создать пользователя: статус {response_create_user.status_code}, "
            f"ответ: {response_create_user.text}"
        )

    yield response_create_user, [login, password, name]

    CourierHelper.delete_user(response_create_user)