# Открытие двери

from aiogram import types
from handlers.api_service import post_request
from aiogram import Dispatcher

async def open_door_handler(message: types.Message):

    domofons = message.bot.get("domofons", [])
    tenant_id = message.bot.get("tenant_id")
    domofon_name = message.text.split(" ")[-1]

    selected_domofon = next((d for d in domofons if d ["name"] == domofon_name), None)

    if not selected_domofon:
        await message.answer("Домофон не найден.")
        return
    data = {"tenant_id": tenant_id, "door_id": 0}
    response = post_request(f"domo.domofon/, {selected_domofon['id']}/open", data)
    if response:
        await message.answer(f"Дверь домофона '{domofon_name}' успешно открыта!")
    else:
        await message.answer(f"Ошибка при открытии двери домофона '{domofon_name}'.")

def register_open_door_handler(dp: Dispatcher):
    dp.register_message_handler(open_door_handler, commands=['Открыть дверь'])
