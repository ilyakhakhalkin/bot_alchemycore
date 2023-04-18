import abc

from markup.markup import Keyboard
from data_base.dbalchemy import DBManager


class Handler(metaclass=abc.ABCMeta):

    def __init__(self, bot) -> None:
        self.bot = bot
        self.keyboard = Keyboard()
        self.DB = DBManager()

    @abc.abstractmethod
    def handle(self):
        pass
