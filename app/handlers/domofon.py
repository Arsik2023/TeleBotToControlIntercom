from aiogram import types
from handlers.api_service import post_request
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import Dispatcher


back_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
back_keyboard.add(KeyboardButton('Назад'))

# Обработчик для получения снимка с камеры епта сучка
async def get_domofon_image_handler(message: types.Message):
    print(f"Обработчик вызван для: {message.text}")
    domofons = message.bot.get("domofons", [])
    tenant_id = message.bot.get("tenant_id")
    domofon_name = message.text

    # Проверяем, выбран ли домофон из доступных вариков
    selected_domofon = next((d for d in domofons if d["name"] == domofon_name), None)

    if not selected_domofon:
        await message.answer("Выбранный домофон не найден. Попробуйте снова.", reply_markup=back_keyboard)
        return

    # Запрос к API
    data = {
        "intercoms_id": [selected_domofon["id"]],
        "media_type": ["JPEG"]
    }
    response = post_request("domo.domofon/urlsOnType", data, params={"tenant_id": tenant_id})

    if response:
        print("Ответ от API:", response)
        if len(response) == 0:  # Если API вернул пустой список
            await message.answer(f"Для домофона {domofon_name} нет доступных снимков.")
        else:
            # Обрабатываем первый элемент нашего блядского ответа
            result = response[0]
            image_url = result.get("jpeg", None)
            hls_url = result.get("hls", None)
            rtsp_url = result.get("rtsp", None)

            # Отправляем изображение, если оно типа есть
            if image_url:
                await message.answer_photo(image_url, caption=f"Снимок с камеры {domofon_name}.")
            else:
                await message.answer("Не удалось получить изображение.", reply_markup=back_keyboard)

            # Отправляем потоковые ссылки, если доступны
            if hls_url or rtsp_url:
                streams = []
                if hls_url:
                    streams.append(f"HLS поток: {hls_url}")
                if rtsp_url:
                    streams.append(f"RTSP поток: {rtsp_url}")
                await message.answer("\n".join(streams))
    else:
        print("Ошибка при получении данных от API")
        await message.answer("Ошибка при получении снимка с камеры.", reply_markup=back_keyboard)

# обработчик
def register_domofon_handler(dp: Dispatcher):
    dp.register_message_handler(
        get_domofon_image_handler,
        lambda message: message.text in [d["name"] for d in message.bot.get("domofons", [])]
    )
