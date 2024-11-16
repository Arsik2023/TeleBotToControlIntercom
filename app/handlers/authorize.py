from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from handlers.keyboards import create_main_menu_keyboard , create_back_keyboard
from aiogram import Dispatcher
from handlers.api_service import post_request
from handlers.database import Add_user, get_user  # Импорт работы с базой данных

# Клавиатуры
retry_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
retry_keyboard.add(KeyboardButton('Отправить контакт', request_contact=True))
authorized_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
authorized_keyboard.add(KeyboardButton('Показать домофоны'))

# Функция для авторизации пользователя
async def auth_user(phone_number):
    """
    Авторизация пользователя через API.
    """
    data = {'phone': phone_number}
    response = post_request('check-tenant', data)
    if response is not None and "tenant_id" in response:
        return response["tenant_id"]
    return None

# Обработчик для команды /star

async def start_handler(message: types.Message):
    """
    Обработчик команды /start. Проверяет, есть ли пользователь в базе данных.
    """
    username = message.from_user.username
    user_data = get_user(username)

    # Приветственное сообщение
    welcome_message = (
        "Добро пожаловать в наш Telegram-бот!\n\n"
        "С помощью этого бота вы можете управлять домофонами и получать удобный доступ к связанным сервисам.\n\n"
        "Пожалуйста, отправьте ваш номер телефона для авторизации или выберите доступные опции ниже."
    )

    if user_data:
        tenant_id, phone_number = user_data
        print(f"[DEBUG] Пользователь найден в базе данных: tenant_id={tenant_id}")
        message.bot["tenant_id"] = tenant_id  # Устанавливаем tenant_id
        await message.answer(
            f"{welcome_message}\n\n"
            f"Вы уже зарегистрированы, {username}!\n\n"
            f"Ваш tenant_id: {tenant_id}\n"
            f"Номер телефона: {phone_number}\n\n",
            reply_markup=create_main_menu_keyboard()
        )
    else:
        print("[DEBUG] Пользователь не найден в базе данных")
        await message.answer(
            "Добро пожаловать! Пожалуйста, отправьте ваш номер телефона для авторизации.",
            reply_markup=create_back_keyboard()
        )

# Обработчик для получения контакта пользователя
async def contact_handler(message: types.Message):
    """
    Обработчик для получения контакта пользователя.
    """
    phone_number = message.contact.phone_number
    if phone_number.startswith("+7"):
        phone_number = phone_number[1:]
    elif phone_number.startswith("8"):
        phone_number = f"7{phone_number[1:]}"

    # Авторизация пользователя через API
    tenant_id = await auth_user(phone_number)

    if tenant_id:
        username = message.from_user.username
        if Add_user(username, tenant_id, phone_number):
            message.bot["tenant_id"] = tenant_id
            await message.answer(
                f"Авторизация успешна! Ваш tenant_id: {tenant_id}.",
                reply_markup=authorized_keyboard
            )
        else:
            await message.answer("Вы уже зарегистрированы.", reply_markup=authorized_keyboard)
    else:
        await message.answer(
            "Ошибка авторизации. Попробуйте позже.",
            reply_markup=retry_keyboard
        )

# Регистрация обработчиков
def register_authorize_handler(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["start"])
    dp.register_message_handler(contact_handler, content_types=types.ContentType.CONTACT)
