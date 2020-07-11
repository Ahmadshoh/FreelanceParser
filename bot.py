import telebot

token = '975829266:AAHpFXyeGSfBNv-jpfYwUwsLPMph4DCDxK4'
bot = telebot.TeleBot(token)

keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row("Привет", "Пока", "Досвидос")
keyboard.row("Как дела?")


def send(chat_id, text):
    bot.send_message(chat_id, text, reply_markup=keyboard)


@bot.message_handler(commands=['start'])
def answer(message):
    send(message.chat.id, "Hello world!")


@bot.message_handler(content_types=['text'])
def main(message):
    chat_id = message.chat.id
    msg = message.text

    if msg == "Привет":
        send(chat_id, "Hi")
    else:
        send(chat_id, "Пашол блять")


bot.polling(none_stop=True)
