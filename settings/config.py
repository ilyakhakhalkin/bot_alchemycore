import os
from emoji import emojize
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv('DEBUG')
TOKEN = os.getenv('TOKEN')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
DEFAULT_ADMINS = os.getenv('DEFAULT_ADMINS')
GRANT_PERM_COMMAND = os.getenv('GRANT_PERM_COMMAND')
REMOVE_PERM_COMMAND = os.getenv('REMOVE_PERM_COMMAND')
LOAD_DATA_COMMAND = os.getenv('LOAD_DATA_COMMAND')
NAME_DB = os.getenv('NAME_DB')
VERSION = os.getenv('VERSION')
AUTHOR = os.getenv('AUTHOR')

DB_ENGINE = os.getenv('DB_ENGINE')
DB_NAME = os.getenv('DB_NAME')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE = os.path.join(
    f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)

if DEBUG:
    DATABASE = os.path.join('sqlite:///' + BASE_DIR, NAME_DB)

COUNT = 0

VK_PERSONAL_LINK = 'https://vk.com/tat_hah'
VK_COMMUNITY_LINK = 'https://vk.com/lernenwirdeutsch'


KEYBOARD = {
    'SETTINGS': emojize(':gear: Настройки'),
    'TEST_LIST': emojize(':check_mark: Пройти тест'),
    'CONTACTS': emojize(':telephone: Контакты'),
    'ABOUT': emojize(':woman: Обо мне'),
    'REQUEST_TEACHER': emojize(':teacher: Записаться на бесплатную встречу'),
    'DECLINE_TEACHER': emojize('Нет, спасибо'),
    'MAIN_MENU': emojize('Главное меню'),
    'MY_RESULTS': emojize('Мои результаты')
}

COMMANDS = {
    'START': 'start',
    'HELP': 'help',
}

QUIZ_LEVELS = {}

QUIZ_GRADE_RANGE = {
    'BAD_GRADE': [0, 35],
    'GOOD_GRADE': [36, 70],
    'PERFECT_GRADE': [70, 100],
}
