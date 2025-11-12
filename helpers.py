import random
import string
import logging
import requests
from urls import Urls

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class CourierHelper:

    @staticmethod
    def email_address():
        email = "ivan" + str(random.randint(1000,1000000)) + '@yandex.ru'
        return email

    @staticmethod
    def generate_random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    @staticmethod
    def delete_user(response_create_user):
        try:
            access_token = response_create_user.json().get("accessToken")
            if access_token:
                headers = {"Authorization": access_token}
                response = requests.delete(f"{Urls.BASE_URL}{Urls.AUTH_USER}", headers=headers)
                if response.status_code != 202:
                    logging.warning(
                        f"Пользователь не удалён. Статус: {response.status_code}. Ответ: {response.text}"
                    )
                else:
                    logging.info(f"Пользователь успешно удалён. login={response_create_user.json().get("user").get('email')}")
            else:
                logging.warning("accessToken отсутствует в ответе. Удаление не выполнено.")
        except Exception as e:
            logging.error(f"Ошибка при удалении пользователя: {e}")
