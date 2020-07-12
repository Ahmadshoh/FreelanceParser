import requests
from bs4 import BeautifulSoup as BS
import re
import telebot


max_page = 3
pages = []
token = '975829266:AAHpFXyeGSfBNv-jpfYwUwsLPMph4DCDxK4'

bot = telebot.TeleBot(token)
keyboard = telebot.types.ReplyKeyboardMarkup(True)

keyboard.row("Посмотреть новые проекты")


def clean_html(query):
    processed_query = re.compile('<.*?>')
    cleaned_text = re.sub(processed_query, '', query)

    return cleaned_text


def parse_from_kwork(chat_id):
    for x in range(max_page + 1, 0, -1):
        pages.append(requests.get('https://kwork.ru/projects?page=' + str(x)))

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

            message = f"Название проекта: <b>{title}</b>\n\n"
            message += f"Логин заказчика: <b>{customer}</b>\n\n"
            message += f"Описание заказа: <b>{description}</b>\n\n"
            message += f"{price}\n\n"
            message += f"Услугу предложили {suggestions[1]} человек"

            send(chat_id, message)


def send(chat_id, text):
    bot.send_message(chat_id, text, reply_markup=keyboard, parse_mode='html')


@bot.message_handler(content_types=['text'])
def main(message):
    chat_id = message.chat.id
    msg = message.text

    if msg == "Посмотреть новые проекты":
        parse_from_kwork(chat_id)


bot.polling(none_stop=True)
