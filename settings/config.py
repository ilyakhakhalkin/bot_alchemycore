import os
from pathlib import Path

from emoji import emojize
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv('DEBUG', default=False)
TOKEN = os.getenv('TOKEN')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
DEFAULT_ADMINS = os.getenv('DEFAULT_ADMINS')

LOAD_DATA_COMMAND = os.getenv('LOAD_DATA_COMMAND')
BLOCK_USER_COMMAND = os.getenv('BLOCK_USER_COMMAND')
UNBLOCK_USER_COMMAND = os.getenv('UNBLOCK_USER_COMMAND')
GET_STAT_COMMAND = os.getenv('GET_STAT_COMMAND')

NAME_DB = os.getenv('NAME_DB')
VERSION = os.getenv('VERSION')
AUTHOR = os.getenv('AUTHOR')

DB_ENGINE = os.getenv('DB_ENGINE')
DB_NAME = os.getenv('DB_NAME')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE = os.path.join(
    f'{DB_ENGINE}{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)

EXCEL_FOLDER = 'excel_files'


if DEBUG:
    TOKEN = os.getenv('DEV_TOKEN')
    ENGINE_DB = os.getenv('ENGINE_DB')
    DATABASE = os.path.join(f'{ENGINE_DB}{BASE_DIR}', NAME_DB)


KEYBOARD = {
    'SETTINGS': emojize(':gear: Настройки'),
    'TEST_LIST': emojize(':check_mark: Пройти тест'),
    'CONTACTS': emojize(':telephone: Контакты'),
    'ABOUT': emojize(':woman: Обо мне'),
    'REQUEST_TEACHER': emojize(':teacher: Записаться на бесплатную встречу'),
    'DECLINE_TEACHER': emojize('Нет, спасибо'),
    'MAIN_MENU': emojize('Главное меню'),
    'MY_RESULTS': emojize('Мои результаты'),
    'COMPLETE_QUIZ': emojize(':face_with_peeking_eye: Закончить тест')
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

ANSWER_LABELS = {
    True: '+',
    None: 'N/A',
    False: '-'
}

ANSWER_COLORS = {
    '+': 'background-color : green',
    '-': 'background-color : lightskyblue',
}
