import asyncio
import logging

import aiogram.types
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup
from imports.config import *
from imports.Support import Support

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
support = Support()


async def on_bot_start_up(dispatcher: Dispatcher) -> None:
    asyncio.create_task(background_job_refresh_data())


async def background_job_refresh_data() -> None:
    while True:
        await asyncio.sleep(WORKER_DELAY_IN_SECONDS)
#        support.update_data_frame()


@dp.message_handler(commands=['start'])
async def show_start(message: types.Message):
    if support.users.is_telegram_id_exists(message.from_user.id):
        new_first_markup = support.create_standard_markup('')
        await message.answer(text=f'Здравствуйте, {message.from_user.first_name}')
        await message.answer(text='это бот базы знаний. Выберите раздел',
                             reply_markup=new_first_markup)
    else:
        markup = support.create_contact_markup()
        await message.answer(text=GREETING_TEXT, reply_markup=markup)


@dp.message_handler(content_types=['contact'])
async def contact(message: types.Message):
    if message.contact is not None:
        if support.users.is_phone_number_exists(message.contact.phone_number):
            support.users.update_telegram_id(message.contact.phone_number, message.from_user.id)
            new_first_markup = support.create_standard_markup('')
            await message.answer(text=f'Здравствуйте, {message.contact.first_name}',
                                 reply_markup=aiogram.types.ReplyKeyboardRemove())
            await message.answer(text='это бот базы знаний. Выберите раздел',
                                 reply_markup=new_first_markup)
        else:
            await message.answer(text='Ваш номер телефона не найден в базе. Обратитесь к вашему супервайзеру.')


@dp.callback_query_handler()
async def process_callbacks(callback_query: types.CallbackQuery):
    """Handling a response to a button click"""
    await callback_query.answer(callback_query.id)
    if not callback_query.data.startswith(BUTTON_PREFIX):
        await bot.send_message(callback_query.from_user.id,
                               text='Устаревшая версия кнопок, сотрите историю и начните заново')
        return
    query = callback_query.data[len(BUTTON_PREFIX):].strip('_')
    children = support.get_children(query)
    if len(children) > 0:
        markup = support.create_standard_markup(query)
        text = support.replace_ids_with_names(query)
        await bot.send_message(callback_query.from_user.id, text=text, reply_markup=markup)
    else:
        text = support.get_answer(query)
        markup = support.create_repeat_markup(query)
        await bot.send_message(callback_query.from_user.id, text=text, parse_mode='HTML', reply_markup=markup)


@dp.message_handler()
async def echo(message: types.Message):
    """Handling a response to a text query"""
    if support.users.is_telegram_id_exists(message.from_user.id):
        markup = InlineKeyboardMarkup()
        text = support.get_answer(message.text.strip())
        if text != NOT_FOUND_ANSWER:
            markup = support.create_repeat_markup(message.text)
        await message.answer(text=text, parse_mode='HTML', reply_markup=markup)
    else:
        markup = support.create_contact_markup()
        await message.answer(text=GREETING_TEXT, reply_markup=markup)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S')
#    support.update_data_frame(start=True)
    executor.start_polling(dp, skip_updates=True, on_startup=on_bot_start_up)
