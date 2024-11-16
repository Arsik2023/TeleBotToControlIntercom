from aiogram import types
from handlers.api_service import get_request
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import Dispatcher

# Клавиатура для возврата
back_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
back_keyboard.add(KeyboardButton('Назад'))

async def select_apartament_handler(message:types.Message):
    print("[DEBUG] Обработчик вызван для выбора квартиры")

    tenant_id =  message.bot.get("tenant_id")
    response = get_request("apartment", params={"tenant_id": tenant_id})

    if not response or len(response) == 0:
        await message.answer("У вас нет квартир. Пожалуйста, свяжитесь с администратором.")
        return
    
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for zxc in response:
        keyboard.add(KeyboardButton(text=f'{zxc["name"]}'))

    await message.answer("Выберите квартиру:", reply_markup=keyboard)
    message.bot["apartmets"] = response
    
# Функция для создания клавиатуры с домофонами
def create_domofon_keyboard(domofons):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for zxc in domofons:  # ZXC
        keyboard.add(KeyboardButton(text=f'{zxc["name"]}'))
    return keyboard

async def list_domofon_handlers(message: types.Message):
    print("Обработчик вызван для кнопки Показать домофоны")
    tenant_id = message.bot.get('tenant_id')
    
    if not tenant_id:
        await message.answer("Вы не авторизованы. Пожалуйста, начните с команды /start")
        return
    
    response = get_request("domo.apartment", params={"tenant_id": tenant_id})

    if response:
        print("Ответ от API", response)
        domofons = [{"id": d["id"], "name": d["name"]} for d in response]
        message.bot["domofons"] = domofons
        domofon_keyboard = create_domofon_keyboard(domofons)
        await message.answer("Выберите домофон:", reply_markup=domofon_keyboard)
    else:
        print("Ошибка получения данных от API")
        await message.answer("Ошибка получения списка домофонов.", reply_markup=back_keyboard)

def register_apartament_handler(dp: Dispatcher):
    dp.register_message_handler(list_domofon_handlers, text="Показать домофоны")