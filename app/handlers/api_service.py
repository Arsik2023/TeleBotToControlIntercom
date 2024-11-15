# эта наш модуль(файл) для работы с api домофона . Реализует Get и Post - запросы

import requests
DOMO_API_URL = "https://domo-dev.profintel.ru/tg-bot"

API_KEY = "SecretToken"

def get_request(endpoint, params=None):
    url = f"{DOMO_API_URL}/{endpoint}"
    headers = {
        "x-api-key": API_KEY,  # Добавляем обязательный заголовок
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Проверяем статус ответа
        return response.json()  # Возвращаем JSON-ответ
    except requests.RequestException as e:
        print(f"Ошибка при выполнении GET-запроса: {e}")
        return None

def post_request(endpoint, data, params=None):
    url = f"{DOMO_API_URL}/{endpoint}"
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    try:
        print(f"URL: {url}")
        print(f"Headers: {headers}")
        print(f"Query Params: {params}")
        print(f"Body: {data}")

        # Отправляем запрос
        response = requests.post(url, json=data, headers=headers, params=params)
        response.raise_for_status()  # Проверяем статус ответа
        print(f"Ответ от API: {response.text}")  # Логируем тело ответа
        return response.json()  # Возвращаем JSON-ответ
    except requests.HTTPError as e:
        print(f"Ошибка HTTP: {e}")
        print(f"Тело ответа: {response.text}")  # Логируем тело ответа при ошибке
        return None