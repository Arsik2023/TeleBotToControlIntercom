 # Точка входа. Здесь будет запускаться бот  и все обработчики

from aiogram import Bot , Dispatcher
from aiogram.utils import executor
from handlers.start import register_handlers_start
from handlers.authorize import register_authorize_handler
from handlers.apartament import register_apartament_handler
from handlers.domofon import register_domofon_handler
from handlers.open import register_open_door_handler


TOKEN = "7317252711:AAFf0mWk7yA4hfQNWuD_UZ20GXfq8dgJxOQ"

qwe = """
            (          
     )      )\ )    )  
  ( /(    )(()/( ( /(  
  )\())( /( /(_)))\()) 
 ((_)\ )\()|_))_((_)\  
 /  (_|(_)\| |_ | |(_) 
| () |\ \ /| __|| / /  
 \__/ /_\_\|_|  |_\_\  
                       
"""
print(qwe)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

register_handlers_start(dp)
register_authorize_handler(dp)
register_apartament_handler(dp)
register_domofon_handler(dp)
register_open_door_handler(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)