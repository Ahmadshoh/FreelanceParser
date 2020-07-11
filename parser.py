import requests
from bs4 import BeautifulSoup as BS
import webbrowser as wb
import re

max_page = 2
pages = []
token = "528348308:AAGgCbTj4g5bTku8vGQ4Adt74U-Kr7qLFXI"
chat_id = "-278992946"


def clean_html(query):
    processed_query = re.compile('<.*?>')
    cleaned_text = re.sub(processed_query, '', query)

    return cleaned_text


for x in range(1, max_page + 1):
    pages.append(requests.get('https://kwork.ru/projects?c=37&page=' + str(x)))


for r in pages:
    html = BS(r.content, 'html.parser')

    for el in html.select('.card'):
        title = el.select('.wants-card__header-title > a')
        title = clean_html(str(title[0]))

        description = el.select('.js-want-block-toggle-full')
        if not description:
            description = el.select('.f14')
        description = clean_html(str(description[0]).replace('<a class="js-want-link-toggle-desc link_local" href="javascript:void(0);">Скрыть</a>', ""))

        price = el.select('.wants-card__price')
        price = clean_html(str(price[0]))

        customer = el.select('.dib > a')
        customer = clean_html(str(customer[0]))

        suggestions = el.select('.query-item__info')
        suggestions = suggestions[0].text.split("Предложений:")

        message = f"Название проекта: <b>{title}</b>%0A%0A"
        message += f"Логин заказчика: <b>{customer}</b>%0A%0A"
        message += f"Описание заказа: <b>{description}</b>%0A%0A"
        message += f"{price}%0A%0A"
        message += f"Поступило предложения: {suggestions[1]}"

        sendToTelegram = wb.open(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&parse_mode=html&text={message}", "r")

        if sendToTelegram:
            print('Success')
        else:
            print("Error")
