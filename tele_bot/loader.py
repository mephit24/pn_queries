from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.db_api.test_conn import get_list_tgusers

from data import config


bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

DB_CREDIENTALS = config.DB_CREDIENTALS

tgusers = get_list_tgusers(DB_CREDIENTALS)
