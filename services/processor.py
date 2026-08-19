import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib3
from .scraper import get_lots_from_html
from datetime import datetime


# ОТКЛЮЧАЕМ ПРЕДУПРЕЖДЕНИЯ SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def request_html(url: str, params: dict) -> str | None:
    # Заголовки, чтобы имитировать запрос от браузера
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

    # Настройка повторных попыток при ошибках (на случай временных сбоев)
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        # Выполняем GET-запрос
        response = session.get(
            url,
            params=params,
            headers=headers,
            timeout=15,
            verify=False
        )
        print(f"Запрос: {response.url}")
        print(f"Статус: {response.status_code}")
        # Проверяем статус ответа
        response.raise_for_status()  # Вызовет исключение для кодов 4xx/5xx
        response.encoding = 'utf-8'
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при запросе: {e}")
        return None


def get_lots(base_url: str, params_dict: dict, translation: dict, default_params: dict) -> list[dict]:
    their_params_dict = params_dict.copy() #это локальная копия с данными под формат сайта к которму делаются запросы
    phrases = [phrase.strip() for phrase in their_params_dict['phrases'].split(',')] if their_params_dict['phrases'] else ''
    if their_params_dict['date_min']:
        dt = datetime.strptime(their_params_dict['date_min'], "%Y-%m-%d")
        their_params_dict['date_min'] = dt.strftime("%d.%m.%Y")
    if their_params_dict['date_max']:
        dt = datetime.strptime(their_params_dict['date_max'], "%Y-%m-%d")
        their_params_dict['date_max'] = dt.strftime("%d.%m.%Y")
    lots = []
    clear_params = default_params
    for param in their_params_dict:
        if param != 'phrases' and their_params_dict[param]:
            if isinstance(their_params_dict[param], list):
                for val in their_params_dict[param]:
                    clear_params.update({translation[val]: 'on'})
            else:
                clear_params.update({translation[param]: their_params_dict[param]})
    if phrases:
        for phrase in phrases:
            request_params = clear_params | {translation['phrase']: phrase}
            response_html = request_html(url=base_url, params=request_params)
            requst_lots = get_lots_from_html(response_html)
            lots += requst_lots
    else:
        response_html = request_html(url=base_url, params=clear_params)
        requst_lots = get_lots_from_html(response_html)
        lots += requst_lots
    print("Запросы выполнены")
    return lots        



    
if __name__ == "__main__":
    # URL для запроса
    url = "https://zakupki.gov.ru/epz/order/extendedsearch/results.html"
    # Параметры запроса (все, что после '?')
    params = {
        "searchString": "бытовая техника",
        "morphology": "on",
        "search-filter": "Дате размещения",
        "pageNumber": "1",
        "sortDirection": "false",
        "recordsPerPage": "_10",
        "showLotsInfoHidden": "false",
        "sortBy": "UPDATE_DATE",
        "fz44": "on",
        "fz223": "on",
        "af": "on",
        "ca": "on",
        "pc": "on",
        "pa": "on",
        "priceFromGeneral": "400000",
        "priceToGeneral": "1000000",
        "currencyIdGeneral": "-1",
        "applSubmissionCloseDateFrom": "19.08.2026",
        "applSubmissionCloseDateTo": "22.08.2026"
    }

    print(request_html(url, params)[:300])