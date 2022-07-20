import configparser
from pathlib import Path
from re import split as re_split

# Get config from config.ini
pathdirconf = Path(__file__).parent.parent.parent
common_config = configparser.ConfigParser()
common_config.read(f"{pathdirconf}\config.ini")
tg_section_config = common_config['TELEGRAM_BOT']
db_section_config = common_config['POSTGRES_DB']

BOT_TOKEN = tg_section_config.get('BOT_TOKEN')
ADMINS = tuple(re_split('/D+', tg_section_config.get('ADMINS')))
IP = tg_section_config.get('ip')

DB_CREDIENTALS = {i: db_section_config.get(i) for i in db_section_config}
