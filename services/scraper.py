from bs4 import BeautifulSoup
import re
from typing import List, Dict, Any


def get_lots_from_html(html: str) -> List[Dict[str, Any]]:
    """
    Парсит HTML-страницу с результатами поиска закупок и возвращает список словарей с данными о закупках.
    """
    if not html:
        return []
    
    soup = BeautifulSoup(html, 'lxml')
    lots = []
    
    # Ищем все блоки с закупками
    entries = soup.select('.search-registry-entry-block')
    
    for entry in entries:
        try:
            # Извлекаем номер закупки
            number_elem = entry.select_one('.registry-entry__header-mid__number a')
            if number_elem:
                lot_id = number_elem.get_text(strip=True)
                lot_href = number_elem.get('href')
            else:
                lot_id = "Номер закупки не найден"
                lot_href = None
            
            # Извлекаем стоимость
            cost_elem = entry.select_one('.price-block__value')
            if cost_elem:
                cost = cost_elem.get_text(strip=True)
            else:
                cost = "Стоимость не найдена"
            
            # Извлекаем объект закупки
            item_elem = entry.select_one('.registry-entry__body-value')
            if item_elem:
                # Получаем текст, убираем лишние пробелы
                item = ' '.join(item_elem.get_text(strip=True).split())
            else:
                item = "Объект закупки не найден"
            
            # Извлекаем заказчика
            customer_elem = entry.select_one('.registry-entry__body-href a')
            if customer_elem:
                customer = ' '.join(customer_elem.get_text(strip=True).split())
            else:
                customer = "Заказчик не найден"
            
            lots.append({
                'id': lot_id,
                'href': lot_href,
                'cost': cost,
                'item': item,
                'customer': customer
            })
            
        except Exception as e:
            # Логируем ошибку, но продолжаем парсинг
            print(f"Ошибка при парсинге закупки: {e}")
            continue
    
    return lots


if __name__ == "__main__":
    from processor import request_html
    # Пример использования
    # Сначала нужно получить HTML через request_html
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
        "currencyIdGeneral": "-1"
    }

    html = request_html(url, params)
    lots = get_lots_from_html(html)
    print(lots)