from emoji import emojize
from telebot.types import KeyboardButton
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

from settings import config
from data_base.dbalch import DBManager


class Keyboard:
    def __init__(self) -> None:
        self.markup = None
        self.DB = DBManager()

    def set_btn(self, name):
        return KeyboardButton(config.KEYBOARD[name])

    def remove_menu(self):
        return ReplyKeyboardRemove()

    def start_menu(self):
        self.markup = ReplyKeyboardMarkup(True, True, row_width=2)
        test_btn = self.set_btn('TEST_LIST')
        contact_btn = self.set_btn('CONTACTS')
        info_btn = self.set_btn('ABOUT')

        self.markup.row(test_btn, info_btn, contact_btn)

        return self.markup

    def test_list_menu(self):
        self.markup = ReplyKeyboardMarkup(True, True, row_width=2)
        quizzes = self.DB.get_quizzes()

        buttons = []
        for q in quizzes:
            config.KEYBOARD['LEVEL_' + q.name] = emojize(':star: ' + q.name)
            config.QUIZ_LEVELS[emojize(':star: ' + q.name)] = q.id

            buttons.append(self.set_btn('LEVEL_' + q.name))

        main_menu = self.set_btn('MAIN_MENU')

        self.markup.row(*buttons, main_menu)

        return self.markup

    def quiz_menu(self):
        self.markup = ReplyKeyboardMarkup(True, True, row_width=2)
        main_menu = self.set_btn('MAIN_MENU')

        self.markup.row(main_menu)

        return self.markup

    def go_back_to_main(self):
        self.markup = ReplyKeyboardMarkup(True, True, row_width=2)
        main_menu = self.set_btn('MAIN_MENU')

        self.markup.row(main_menu)

        return self.markup

    def request_teacher_markup(self):
        self.markup = ReplyKeyboardMarkup(True, True, row_width=2)

        request_btn = self.set_btn('REQUEST_TEACHER')
        decline_btn = self.set_btn('DECLINE_TEACHER')

        self.markup.row(request_btn)
        self.markup.row(decline_btn)

        return self.markup
