from emoji import emojize

from .config import VK_COMMUNITY_LINK, VK_PERSONAL_LINK

START_MSG = 'Привет, {}! Здесь ты можешь проверить свои знания немецкого языка на уровнях A1 - B1.'
CHOOSE_LEVEL_MSG = 'Ты можешь выбрать уровень:'
RESULT_STAT_MSG = 'Результат: {}/{}, {}% правильных ответов.'
ASK_TEACHER_REQUEST = 'Хочешь обсудить результат теста с преподавателем и подобрать для тебя подходящий формат занятий?'
TEACHER_REQUESTED = 'Твоя заявка передана преподавателю, тебе придет личное сообщение в течение 24 часов.'
ASK_NEXT_QUIZ = 'Хочешь проверить следующий уровень?'
THANKS_AND_INVITE = f"""Благодарю за прохождение теста!\nБуду рада твоему участию в группе {VK_COMMUNITY_LINK}.
Добавляйся в друзья: {VK_PERSONAL_LINK}"""

ABOUT = f'''Привет! Рада, что ты здесь))
⭐ Помогаю в изучении немецкого для твоих самых смелых целей:
- работа, учеба, переезд на ПМЖ,
- подготовимся к экзаменам,
- улучшим успеваемость в школе или ВУЗе. 

Со мной ты сможешь 
* повысить свой уровень владения немецким языком 💪,
* получать удовольствие от занятий и своего прогресса,
* заниматься в своем темпе, осваивая новое поэтапно

🚀 Мои основные продукты и услуги:
- общий курс разговорного немецкого языка
- курс подготовки к поездке, встрече, событию
- курс грамматики

Занятия проводятся индивидуально, в паре и мини-группе, онлайн (skype, zoom).

Если хочешь спросить об этом подробнее, напиши мне в личные сообщения {VK_PERSONAL_LINK}'''

CONTACTS = f'''Telegram: @tat_hah
Группа ВК: {VK_COMMUNITY_LINK}\n
Страница ВК: {VK_PERSONAL_LINK}
'''

BAD_GRADE = ':3rd_place_medal: Маловато баллов, этот уровень нужно пройти сначала.'
GOOD_GRADE = ':2nd_place_medal: Хорошо, но нужно кое-что повторить.'
PERFECT_GRADE = ':1st_place_medal: Ты молодец! Отлично!'


MESSAGES = {
    'START_MSG': START_MSG,
    'CHOOSE_LEVEL': CHOOSE_LEVEL_MSG,
    'RESULT_STAT': RESULT_STAT_MSG,
    'BAD_GRADE': emojize(BAD_GRADE),
    'GOOD_GRADE': emojize(GOOD_GRADE),
    'PERFECT_GRADE': emojize(PERFECT_GRADE),
    'ASK_TEACHER_REQUEST': ASK_TEACHER_REQUEST,
    'ASK_NEXT_QUIZ': ASK_NEXT_QUIZ,
    'THANKS_AND_INVITE': THANKS_AND_INVITE,
    'ABOUT': emojize(ABOUT),
    'CONTACTS': CONTACTS,
    'TEACHER_REQUESTED': TEACHER_REQUESTED
}