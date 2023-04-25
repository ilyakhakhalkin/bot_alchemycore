# Quiz telegram bot
## Description
This is a quiz Telegram bot that was made for a German language teacher to provide a testing system for students. As a student, you can take a test, see the results, and optionally send a request to the teacher for consultation. For more detailed information, please refer to the 'Setup' section.

Version 1.4 is the MVP (minimum viable product) version of the project - a simple synchronous system that will be improved in the future. It is not perfect and has not been fully optimized yet. The next tasks will be described in the backlog section.

## Tech stack
- Python
- Telebot (synchronous)
- SQLAlchemy (Core)
- PostgreSQL
- Docker

## Setup
### Python and environment
0. Install Python if you don't have it yet:
```
https://www.python.org/downloads/
```

1. clone repo:
```
git clone https://github.com/ilyakhakhalkin/bot_alchemycore.git
```

2. Create virtual environment:
```
python3 -m venv venv
```

3. Activate virtual environment:
- macos:
```
. venv/bin/activate
```

- win:
```
source venv/Scripts/activate
```

- see also:
```
https://docs.python.org/3/library/venv.html
```

4. Install dependencies:
```
pip3 install -r requirements.txt
```


### App
1. Security-sensitive settings are stored in a .env file. First, rename the .env_sample to .env and keep it at the root of the project.

2. Provide your .env settings:

2.1 TOKEN - If you don't have one, please follow the official Telegram guide:
```
https://core.telegram.org/bots/features#botfather
```
- In DEBUG mode DEV_TOKEN is used
- In other cases, TOKEN is used.
You can put the same token in both variables or register two separate bots - one for production and one for development.

2.2 Admin settings - used for administration purposes.

2.3 Databases:
- In DEBUG mode, SQLite is used. Just provide a filename in NAME_DB (*.sqlite), and you are ready to go.
- In other cases, PostgreSQL is used. It's recommended to change the user and password.

3. Next, move to the settings folder.

- In config.py, you can configure the app setup section:
3.1 The KEYBOARD dict determines the labels of keyboard buttons. Buttons and keyboards are created in the markup module.
3.2 EXCEL_FOLDER determines a folder for xlsx files (quizzes data and sessions requested by the user).
3.3 QUIZ_GRADE_RANGE determines grades.

- In messages.py, you can configure the text of the messages.


## How to use
1. Start the bot:
```
python3 tgbot.py
```

2. Send /start command in the telegram chat with your bot

3. Next, you will need to load quiz data to the database. There are two options:
- to load default quiz_data.xlsx file just send to the chat the LOAD_DATA_COMMAND (specified in .env) on the first line and ADMIN_PASSWORD (also specified in .env) on the second line
- to load your custom xlsx file attach it to a message and provide LOAD_DATA_COMMAND and ADMIN_PASSWORD in a caption

Your custom xlsx file must have same structure as a quiz_data.xlsx (you can find it in the /excel_files directory)

In case of successful authorization your message will disappear. If you still see it, check command, password and list of default admins.

4. After that your bot is ready to use


## Backlog
Todo:
1. Refactor admin functionality
2. Optimize DB requests
3. Move to the SQLAlchemy ORM instead of Core
4. Move to aiogram
5. Implement FSM with Redis instead of SQL db
