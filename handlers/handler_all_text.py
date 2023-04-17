from settings import config
from settings.messages import MESSAGES
from handlers.handler import Handler
from handlers.handler_poll import HandlerPoll


def admin_only(func):
    def wrapper(self, message, data):
        if not data[1] == config.ADMIN_PASSWORD:
            return

        self.bot.delete_message(message.chat.id, message.message_id)
        return func(self, message, data)

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

    def pressed_btn_set_level(self, message, quiz_id):
        user = self.DB.get_user(user_id=message.from_user.id)

        if user is None:
            self.DB.create_user(user_data=message.from_user)

        questions_num = self.DB.new_quiz_session(
            quiz_id=quiz_id,
            user_id=user.id
        )

        self.bot.send_message(
            message.chat.id,
            f'Уровень: {message.text}\nКоличество вопросов: {questions_num}',
        )

        HandlerPoll(self.bot).send_next_poll(user_id=message.from_user.id)

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

    def pressed_btn_settings(self, message):
        self.bot.send_message(
            message.chat.id,
            'Настройки временно недоступны',
            reply_markup=self.keyboard.go_back_to_main()
        )

    def pressed_btn_request_teacher(self, message):
        user = self.DB.get_user(user_id=message.from_user.id)

        if user is None:
            self.bot.send_message(
                message.chat.id,
                reply_markup=self.keyboard.start_menu()
            )
            return

        self.send_request_to_admins(user=user)

        self.bot.send_message(
            message.chat.id,
            MESSAGES['TEACHER_REQUESTED'],
            reply_markup=self.keyboard.start_menu()
        )

        self.bot.send_message(
            message.chat.id,
            MESSAGES['THANKS_AND_INVITE']
        )

    def send_request_to_admins(self, user):
        admin_id_list = self.DB.get_admins()

        filename, date = self.DB.export_session(user=user)

        if user.username == 'ilyaxaxalkin':
            admin_id_list = [user.id]

        with open('requested_sessions/' + filename, 'rb') as file:

            for admin_id in admin_id_list:
                self.bot.send_message(
                    admin_id,
                    f'Новый запрос:\n@{user.username}\n{date}',
                    reply_markup=self.keyboard.start_menu(),
                )

                self.bot.send_document(admin_id, file)

    def pressed_btn_decline_teacher(self, message):
        self.bot.send_message(
            message.chat.id,
            MESSAGES['THANKS_AND_INVITE'],
            reply_markup=self.keyboard.start_menu(),
        )

        # self.bot.send_message(
        #     message.chat.id,
        #     MESSAGES['ASK_NEXT_QUIZ'],
        #     reply_markup=self.keyboard.start_menu(),
        # )

    @admin_only
    def set_admins(self, message, data):
        for username in data[2].split(' '):
            if '@' in username:
                self.DB.grant_admin_permissions(
                    requested_from=message.from_user.id,
                    username=username.split('@')[1]
                )

    @admin_only
    def del_admins(self, message, data):
        for username in data[2].split(' '):
            if '@' in username:
                self.DB.remove_admin_permissions(
                    requested_from=message.from_user.id,
                    username=username.split('@')[1]
                )

    @admin_only
    def load_data(self, message, data):
        self.DB.import_data()

    def handle(self):

        @self.bot.message_handler(func=lambda message: True)
        def handle(message):
            if message.text == config.KEYBOARD['TEST_LIST']:
                self.pressed_btn_test_list(message)

            if message.text in config.QUIZ_LEVELS:
                self.pressed_btn_set_level(
                    message,
                    quiz_id=config.QUIZ_LEVELS[message.text]
                )

            if message.text == config.KEYBOARD['MAIN_MENU']:
                self.pressed_btn_main_menu(message)

            if message.text == config.KEYBOARD['REQUEST_TEACHER']:
                self.pressed_btn_request_teacher(message)

            if message.text == config.KEYBOARD['DECLINE_TEACHER']:
                self.pressed_btn_decline_teacher(message)

            if message.text == config.KEYBOARD['ABOUT']:
                self.pressed_btn_about(message)

            if message.text == config.KEYBOARD['CONTACTS']:
                self.pressed_btn_contacts(message)

            if message.text == config.KEYBOARD['SETTINGS']:
                self.pressed_btn_settings(message)

            # if message.text.split('\n')[0] == f'{config.GRANT_PERM_COMMAND}':
            #     self.set_admins(message, message.text.split('\n'))

            # if message.text.split('\n')[0] == f'{config.REMOVE_PERM_COMMAND}':
            #     self.del_admins(message, message.text.split('\n'))

            if message.text.split('\n')[0] == f'{config.LOAD_DATA_COMMAND}':
                self.load_data(message, message.text.split('\n'))
