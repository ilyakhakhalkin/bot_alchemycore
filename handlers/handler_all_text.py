import os.path

from settings import config
from settings.messages import MESSAGES
from handlers.handler import Handler
from handlers.handler_poll import HandlerPoll


def admin_only(func):
    def wrapper(self, message, text, **kwargs):
        if not text == config.ADMIN_PASSWORD:
            return

        self.bot.delete_message(message.chat.id, message.message_id)
        return func(self, message, text, **kwargs)

    return wrapper


class HandlerAllText(Handler):
    def __init__(self, bot) -> None:
        super().__init__(bot)

    def get_username(self, message):
        if message.from_user.first_name is not None:
            return message.from_user.first_name

        return message.from_user.username

    def pressed_btn_main_menu(self, message):
        self.bot.send_message(
            message.chat.id,
            MESSAGES['START_MSG'].format(self.get_username(message)),
            reply_markup=self.keyboard.start_menu()
        )

    def pressed_btn_test_list(self, message):
        self.bot.send_message(
            message.chat.id,
            MESSAGES['CHOOSE_LEVEL'],
            reply_markup=self.keyboard.test_list_menu(),
        )

    def pressed_btn_set_level(self, message, user, quiz_id):
        questions_num = self.DB.new_quiz_session(
            quiz_id=quiz_id,
            user_id=user.id
        )

        self.bot.send_message(
            user.id,
            f'Уровень: {message.text}\nКоличество вопросов: {questions_num}',
        )
        HandlerPoll.send_next_poll(self, user_id=user.id)

    def pressed_btn_complete_quiz(self, message, user):
        HandlerPoll.complete_quiz(self, user_id=user.id)

    def pressed_btn_about(self, message):
        self.bot.send_message(
            message.chat.id,
            MESSAGES['ABOUT'],
            reply_markup=self.keyboard.go_back_to_main()
        )

    def pressed_btn_contacts(self, message):
        self.bot.send_message(
            message.chat.id,
            MESSAGES['CONTACTS'],
            reply_markup=self.keyboard.go_back_to_main()
        )

    def pressed_btn_request_teacher(self, message, user):
        qsession = self.DB.request_session(user_id=user.id)

        if qsession and self.send_request_to_admins(user=user,
                                                    qsession=qsession):

            if user.username:
                self.bot.send_message(
                    message.chat.id,
                    MESSAGES['TEACHER_REQUESTED'],
                    reply_markup=self.keyboard.start_menu()
                )
            else:
                self.bot.send_message(
                    message.chat.id,
                    MESSAGES['NO_USERNAME'],
                    reply_markup=self.keyboard.start_menu()
                )

            self.bot.send_message(
                message.chat.id,
                MESSAGES['THANKS_AND_INVITE']
            )
            return

        self.bot.send_message(
                message.chat.id,
                MESSAGES['ERROR'],
                reply_markup=self.keyboard.start_menu()
        )

        if not qsession:
            self.bot.send_message(
                    message.chat.id,
                    MESSAGES['NO_SESSION_ERROR'],
                    reply_markup=self.keyboard.start_menu()
            )

    def send_request_to_admins(self, user, qsession):
        admin_id_list = self.DB.get_admins()

        if user.id == '171869564':
            admin_id_list = [user.id]

        caption = 'New request:\n'
        if getattr(user, 'username'):
            caption += '@' + user.username + '\n'

        caption += user.full_name

        for admin_id in admin_id_list:
            with open(qsession.filepath, 'rb') as file:
                self.bot.send_document(
                    admin_id,
                    document=file,
                    caption=caption,
                    reply_markup=self.keyboard.start_menu(),
                )

        return True

    def pressed_btn_decline_teacher(self, message):
        self.bot.send_message(
            message.chat.id,
            MESSAGES['THANKS_AND_INVITE'],
            reply_markup=self.keyboard.start_menu(),
        )

    def get_statistic(self, message):
        unique_users_count = self.DB.get_user_count()

        self.bot.send_message(
            message.from_user.id,
            f'Unique users: {unique_users_count}',
        )

    @admin_only
    def block_user(self, message, text, username_to_block):
        user = self.DB.get_user(username=username_to_block)

        if user is not None:
            print(user.id)
            self.DB.block_user(user_id=user.id)

    @admin_only
    def unblock_user(self, message, text, username_to_unblock):
        user = self.DB.get_user(username=username_to_unblock)

        if user is not None:
            self.DB.unblock_user(user_id=user.id)

    @admin_only
    def load_data(self, message, text, from_message=False):
        if not from_message:
            self.DB.import_data()
            return

        filename = message.document.file_name
        file_info = self.bot.get_file(message.document.file_id)
        downloaded_file = self.bot.download_file(file_info.file_path)

        file_path = os.path.join(
            config.BASE_DIR,
            config.EXCEL_FOLDER, filename
        )

        if not os.path.isdir(
            os.path.join(config.BASE_DIR, config.EXCEL_FOLDER)
        ):
            os.mkdir(
                os.path.join(config.BASE_DIR, config.EXCEL_FOLDER)
            )

        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        self.DB.import_data(path=file_path)
        self.pressed_btn_main_menu(message)

    def handle(self):

        @self.bot.message_handler(func=lambda message: True)
        def handle(message):
            try:
                auth_ = message.text.split('\n')
                command = auth_[0]
                pwd = auth_[1]

            except IndexError:
                command = None

            else:

                if pwd != config.ADMIN_PASSWORD:
                    return

                if command == config.LOAD_DATA_COMMAND:
                    self.load_data(
                        message=message,
                        text=pwd,
                    )

                if command == config.BLOCK_USER_COMMAND:
                    self.block_user(
                        message=message,
                        text=pwd,
                        username_to_block=auth_[2],
                    )

                if command == config.UNBLOCK_USER_COMMAND:
                    self.unblock_user(
                        message=message,
                        text=pwd,
                        username_to_unblock=auth_[2]
                    )

            user = self.DB.get_user(user_id=message.from_user.id)

            if user is None:
                user = self.DB.create_user(user_data=message.from_user)

            elif message.from_user.username != user.username:
                self.DB.update_user(user_data=message.from_user)

            if user.blocked:
                return

            if message.text == config.KEYBOARD['TEST_LIST']:
                self.pressed_btn_test_list(message)

            if message.text in config.QUIZ_LEVELS:
                self.pressed_btn_set_level(
                    message=message,
                    user=user,
                    quiz_id=config.QUIZ_LEVELS[message.text]
                )

            if message.text == config.KEYBOARD['MAIN_MENU']:
                self.pressed_btn_main_menu(message)

            if message.text == config.KEYBOARD['REQUEST_TEACHER']:
                self.pressed_btn_request_teacher(message=message, user=user)

            if message.text == config.KEYBOARD['DECLINE_TEACHER']:
                self.pressed_btn_decline_teacher(message)

            if message.text == config.KEYBOARD['ABOUT']:
                self.pressed_btn_about(message)

            if message.text == config.KEYBOARD['CONTACTS']:
                self.pressed_btn_contacts(message)

            if message.text == config.KEYBOARD['COMPLETE_QUIZ']:
                self.pressed_btn_complete_quiz(message=message, user=user)

            if message.text == config.GET_STAT_COMMAND:
                self.get_statistic(message)

        @self.bot.message_handler(content_types=['document'])
        def handle_file(message):
            try:
                auth_ = message.caption.split('\n')
                command = auth_[0]
                pwd = auth_[1]
            except IndexError:
                return

            else:
                if pwd != config.ADMIN_PASSWORD:
                    return

                if command == config.LOAD_DATA_COMMAND:
                    self.load_data(
                        message=message,
                        text=pwd,
                        from_message=True
                    )
