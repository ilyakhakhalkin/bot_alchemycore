from telebot import TeleBot
from settings import config
from handlers.handler_main import HandlerMain


class TGBot:
    __version__ = config.VERSION
    __author__ = config.AUTHOR

    def __init__(self) -> None:
        self.token = config.TOKEN
        self.bot = TeleBot(self.token)
        self.handler = HandlerMain(self.bot)

    def start(self):
        self.handler.handle()

    def run_bot(self):
        self.start()
        self.bot.polling()


if __name__ == '__main__':

    if config.DEBUG:
        bot = TGBot()
        bot.run_bot()

    else:
        while True:
            try:
                bot = TGBot()
                bot.run_bot()
            except:
                pass
