import requests

# Простой GET запрос
url = "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=%D0%B1%D1%8B%D1%82%D0%BE%D0%B2%D0%B0%D1%8F+%D1%82%D0%B5%D1%85%D0%BD%D0%B8%D0%BA%D0%B0&morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&sortBy=UPDATE_DATE&fz44=on&fz223=on&af=on&ca=on&pc=on&pa=on&priceFromGeneral=400000&priceToGeneral=1000000&currencyIdGeneral=-1&applSubmissionCloseDateFrom=19.08.2026&applSubmissionCloseDateTo=22.08.2026"
response = requests.get(url)

# Проверка статуса
if response.status_code == 200:
    print("Страница загружена успешно!")
    html_content = response.text
    print(html_content[:500])  # Первые 500 символов
else:
    print(f"Ошибка загрузки: {response.status_code}")