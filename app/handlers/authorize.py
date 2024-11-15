from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from handlers.api_service import post_request
from aiogram import Dispatcher

# Клавиатуры
retry_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
retry_keyboard.add(KeyboardButton('Отправить контакт', request_contact=True))
authorized_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
authorized_keyboard.add(KeyboardButton('Показать домофоны'))

# Функция для авторизации пользователя
async def auth_user(phone_number):
    data = {'phone': phone_number}
    response = post_request('check-tenant', data)
    if response is not None and "tenant_id" in response:
        return response["tenant_id"]
    return None

# Обработчик для получения контакта пользователя
async def contact_handler(message: types.Message):
    # Получение и форматирование номера телефона
    phone_number = message.contact.phone_number
    if phone_number.startswith("+7"):
        phone_number = phone_number[1:]
    elif phone_number.startswith("8"):
        phone_number = f"7{phone_number[1:]}"
    
    # Авторизация пользователя
    tenant_id = await auth_user(phone_number)

    if tenant_id:
        print(f"Авторизация успешна: tenant_id={tenant_id}")
        await message.answer(f"Авторизация успешна! Ваш ID: {tenant_id}", reply_markup=authorized_keyboard)
        # Сохраняем tenant_id для дальнейшей работы
        message.bot["tenant_id"] = tenant_id
    else:
        print("Ошибка авторизации")
        await message.answer("Ошибка авторизации. Попробуйте позже.", reply_markup=retry_keyboard)

# Регистрация обработчика
def register_authorize_handler(dp: Dispatcher):
    dp.register_message_handler(contact_handler, content_types=types.ContentType.CONTACT)
