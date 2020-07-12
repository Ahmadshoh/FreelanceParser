import logging
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter
from kwork import KWork


API_TOKEN = '975829266:AAHpFXyeGSfBNv-jpfYwUwsLPMph4DCDxK4'

# задаем уровень логов
logging.basicConfig(level=logging.INFO)
# инициализируем бота
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)
# инициализируем соединение с БД
db = SQLighter('db.db')
# инициализируем парсер
kwork = KWork('last_key.txt')



# Команда активации подписки
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    print(message.from_user.id)
    if not db.subscriber_exists(message.from_user.id):
        # если юзера нет в базе, добавляем его
        db.add_subscriber(message.from_user.id)
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, True)

    await message.answer("Вы успешно подписались на рассылку!\nЖдите, скоро выйдут новые обзоры и вы узнаете о них первыми =)")


# Команда отписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        # если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
        db.add_subscriber(message.from_user.id, False)
        await message.answer("Вы итак не подписаны.")
    else:
        # если он уже есть, то просто обновляем ему статус подписки
        db.update_subscription(message.from_user.id, False)
        await message.answer("Вы успешно отписаны от рассылки.")


# проверяем наличие новых игр и делаем рассылки
async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        # проверяем наличие новых игр
        new_projects = kwork.new_projects()

        if new_projects:
            # если игры есть, переворачиваем список и итерируем
            new_projects.reverse()
            for np in new_projects:
                # парсим инфу о новой игре
                info = kwork.project_info(np)

                # получаем список подписчиков бота
                subscriptions = db.get_subscriptions()

                # отправляем всем новость
                for subscriber in subscriptions:
                    await bot.send_message(
                        subscriber[1],
                        text=info['title'] + "\n\n" + "Описание: " + info['description'] + "\n\n" + info['price'] + "\n" + "Заказал(а): " + info['customer'] + "\n\n" + info['link'],
                        disable_notification=True
                    )

                # обновляем ключ
                kwork.update_last_key(info['id'])


# запускаем лонг поллинг
if __name__ == '__main__':
    dp.loop.create_task(scheduled(10))  # пока что оставим 10 секунд (в качестве теста)
    executor.start_polling(dp, skip_updates=True)
