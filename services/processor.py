import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib3

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
        
        # Проверяем статус ответа
        response.raise_for_status()  # Вызовет исключение для кодов 4xx/5xx
        response.encoding = 'utf-8'
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при запросе: {e}")
        return None


translation = {
    "phrase": "searchString",
    "44-fz": "fz44",
    "223-fz": "fz223",
    'submission-of-applications': 'af',
    'the-work-of-the-Commission': 'ca',
    'purchase-completed': 'pc',
    'purchase-cancelled': 'pa',
    'price_min': 'priceFromGeneral',
    'price_max': 'priceToGeneral',
    'date_min': 'applSubmissionCloseDateFrom',
    'date_max': 'applSubmissionCloseDateTo'
}

const_params = 'morphology=on&search-filter=Дате+размещения&sortDirection=false&pageNumber=1&recordsPerPage=_10&showLotsInfoHidden=false&sortBy=UPDATE_DATE&currencyIdGeneral=-1&'

'''
{'phrases': ['техника', 'школьные парты'], 'law': ['44-fz', '223-fz'], 'purchase_stage': ['submission-of-applications', 'the-work-of-the-Commission', 'purchase-completed', 'purchase-cancelled'], 'price_min': 1234, 'price_max': 3456654, 'date_min': '2026-08-19', 'date_max': '2026-08-28'}
def prepare_params(params, dict):
'''

def get_lots(base_url: str, params_dict: dict, translation: dict, const_params: str) -> list[dict]:
    phrases = params_dict['phrases']
    lots = []
    clear_params = {}
    for param in params_dict:
        if param != 'phrases':
            if isinstance(params_dict[param], list):
                for val in params_dict[param]:
                    clear_params.update({translation[val]: 'on'})
            else:
                clear_params.update({translation[param]: params_dict[param]})
    for phrase in phrases:
        requst_lots = []
        request_params = clear_params | {translation['phrase']: phrase}
        response_html = request_html(url=base_url + const_params, params=request_params)
        



    
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