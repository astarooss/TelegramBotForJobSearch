from aiogram import Bot #класс бота, для анотации типов в функции
from aiogram.dispatcher import Dispatcher #улавливает события в чате и боте
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging



storage = MemoryStorage() # для хранения данных пользователя

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage) #инициализация дисспетчера
logging.basicConfig(level=logging.INFO)

