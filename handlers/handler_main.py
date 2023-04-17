from handlers.handler_command import HandlerCommand
from handlers.handler_all_text import HandlerAllText
from handlers.handler_poll import HandlerPoll


class HandlerMain:
    def __init__(self, bot) -> None:
        self.bot = bot
        self.handler_commands = HandlerCommand(self.bot)
        self.handler_all_text = HandlerAllText(self.bot)
        self.handler_poll = HandlerPoll(self.bot)

    def handle(self):
        self.handler_commands.handle()
        self.handler_all_text.handle()
        self.handler_poll.handle()
