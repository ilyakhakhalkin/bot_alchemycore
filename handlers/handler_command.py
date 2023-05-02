from settings.messages import MESSAGES
from handlers.handler import Handler


class HandlerCommand(Handler):
    def __init__(self, bot) -> None:
        super().__init__(bot)

    def pressed_btn_start(self, message):

        user = self.DB.get_user(user_id=message.from_user.id)

        if user is None:
            user = self.DB.create_user(user_data=message.from_user)

        elif message.from_user.username != user.username:
            self.DB.update_user(user_data=message.from_user)

        if user.blocked:
            return

        self.bot.send_message(
            user.id,
            MESSAGES['START_MSG'].format(user.full_name),
            reply_markup=self.keyboard.start_menu()
        )

    def handle(self):

        @self.bot.message_handler(commands=['start'])
        def handle(message):
            if message.text == '/start':
                self.pressed_btn_start(message)
