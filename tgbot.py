from telebot import TeleBot
from settings import config
from handlers.handler_main import HandlerMain


class TGBot:
    __version__ = config.VERSION

    def __init__(self) -> None:
        self.token = config.TOKEN
        self.bot = TeleBot(self.token)
        self.handler = HandlerMain(self.bot)

    def start(self):
        self.handler.handle()

    def run_bot(self):
        self.start()

        if config.DEBUG:
            self.bot.polling()
        else:
            self.bot.infinity_polling()


if __name__ == '__main__':
    bot = TGBot()
    bot.run_bot()
