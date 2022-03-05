# from environs import Env

# # Теперь используем вместо библиотеки python-dotenv библиотеку environs
# env = Env()
# env.read_env()

# BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
# ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
# IP = env.str("ip")  # Тоже str, но для айпи адреса хоста

import configparser
from pathlib import Path
from re import split as re_split

# Get config from config.ini
pathdirconf = Path(__file__).parent.parent.parent
common_config = configparser.ConfigParser()
common_config.read(f"{pathdirconf}\config.ini")
local_section_config = common_config['TELEGRAM_BOT']

BOT_TOKEN = local_section_config.get('BOT_TOKEN')
ADMINS = tuple(re_split('/D+', local_section_config.get('ADMINS')))
IP = local_section_config.get('ip')



# print(BOT_TOKEN, ADMINS, IP, sep='\n')



