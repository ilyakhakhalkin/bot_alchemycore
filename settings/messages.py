from emoji import emojize


START_MSG = 'Hello, {}!'
CHOOSE_LEVEL_MSG = 'Choose level:'
RESULT_STAT_MSG = 'Result: {}/{}, {}% of right answers.'
ASK_TEACHER_REQUEST = 'Do you want to send request to the teacher?'
TEACHER_REQUESTED = 'Request was sent'
ASK_NEXT_QUIZ = 'Do you want to take another test?'
THANKS_AND_INVITE = 'Thank you for participating'

ABOUT = 'Some info'

CONTACTS = 'Some contacts'

BAD_GRADE = ':3rd_place_medal: Almost good'
GOOD_GRADE = ':2nd_place_medal: Good'
PERFECT_GRADE = ':1st_place_medal: Perfect!'

ERROR_MSG = 'We have got the error on our side :pleading_face:'
SESSION_DOES_NOT_EXISTS = 'You have to take a test first'
NO_USERNAME_IN_REQUEST = 'Request was sent, but you do not have a username, and we cannot contact you directly.'


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
    'NO_SESSION_ERROR': emojize(SESSION_DOES_NOT_EXISTS),
    'NO_USERNAME': emojize(NO_USERNAME_IN_REQUEST),
}
