from emoji import emojize


START_MSG = 'Hello, {}!'
ABOUT = 'Info about'
CONTACTS = 'Contact info'
THANKS_AND_INVITE = 'Thank you for participating'

CHOOSE_LEVEL_MSG = 'Choose level:'
RESULT_STAT_MSG = 'Result: {}/{}, {}% right answers.'
ASK_TEACHER_REQUEST = 'You can send request to a teacher if you want'
TEACHER_REQUESTED = 'Request has been sent'
ASK_NEXT_QUIZ = 'You can take another test if you want'

BAD_GRADE = ':3rd_place_medal: Almost good'
GOOD_GRADE = ':2nd_place_medal: Good'
PERFECT_GRADE = ':1st_place_medal: Perfect'

ERROR_MSG = 'We have an error on our side :pleading_face:'


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
    'TEACHER_REQUESTED': TEACHER_REQUESTED,
    'ERROR': emojize(ERROR_MSG),
}
