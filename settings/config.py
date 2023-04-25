import os
from emoji import emojize
from dotenv import load_dotenv


# APP SETUP
KEYBOARD = {
    'TEST_LIST': emojize(':check_mark: Take a test'),
    'CONTACTS': emojize(':telephone: Contacts'),
    'ABOUT': emojize(':woman: About'),
    'REQUEST_TEACHER': emojize(':teacher: Request teacher'),
    'DECLINE_TEACHER': emojize('No thanks'),
    'MAIN_MENU': emojize('Main menu'),
    'COMPLETE_QUIZ': emojize(':face_with_peeking_eye: Finish test')
}

EXCEL_FOLDER = 'excel_files'
QUIZ_LEVELS = {}

QUIZ_GRADE_RANGE = {
    'BAD_GRADE': [0, 35],
    'GOOD_GRADE': [36, 70],
    'PERFECT_GRADE': [70, 100],
}


# .ENV SETUP
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
ENGINE_DB = os.getenv('ENGINE_DB')
VERSION = os.getenv('VERSION')

DB_ENGINE = os.getenv('DB_ENGINE')
DB_NAME = os.getenv('DB_NAME')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')


# DB SETUP
BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
DATABASE = os.path.join(
    f'{DB_ENGINE}{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)

if DEBUG:
    TOKEN = os.getenv('DEV_TOKEN')
    DATABASE = os.path.join(ENGINE_DB + BASE_DIR, NAME_DB)
