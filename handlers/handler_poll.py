from json import JSONDecoder, JSONEncoder
from random import shuffle
from settings import config
from settings.messages import MESSAGES
from handlers.handler import Handler


class HandlerPoll(Handler):
    def __init__(self, bot) -> None:
        super().__init__(bot)

    @staticmethod
    def send_next_poll(self, user_id):
        user_response = self.DB.get_next_response(user_id=user_id)

        if user_response is None:
            self.complete_quiz(self, user_id=user_id)
            return

        question = self.DB.get_questions(q_id=user_response.question_id)
        options = self.DB.get_answers(q_id_list=[user_response.question_id])
        shuffle(options)

        for i, ans in enumerate(options):
            if ans.is_correct:
                correct_answer_id = i
                break

        sent_message = self.bot.send_poll(
            user_id,
            question=question.text,
            options=[answer.text for answer in options],
            correct_option_id=correct_answer_id,
            type='quiz',
            is_anonymous=False,
            reply_markup=self.keyboard.quiz_menu()
        )

        self.DB.update_response(
            response_id=user_response.id,
            poll_id=int(sent_message.json['poll']['id']),
            options=JSONEncoder().encode(sent_message.json['poll']['options'])
        )

    def poll_answer_received(self, poll_answer):
        user_response = self.DB.get_current_response(
            user_id=poll_answer.user.id,
            poll_id=int(poll_answer.poll_id)
        )

        options = JSONDecoder().decode(s=user_response.options)
        answer_text = options[poll_answer.option_ids[0]]['text']

        answers = self.DB.get_answers(
            q_id_list=[user_response.question_id],
            text=answer_text
        )

        self.DB.update_response(
            response_id=user_response.id,
            answer_id=answers[0].id
        )

        self.send_next_poll(self, user_id=poll_answer.user.id)

    @staticmethod
    def complete_quiz(self, user_id):

        qsession = self.DB.get_quiz_session(user_id=user_id)
        score = self.DB.get_score(qsession=qsession)

        grade = HandlerPoll.estimate_grade(score['percentage'])
        grade_message = MESSAGES[grade]
        text_message = MESSAGES['RESULT_STAT'].format(
            score['points'], score['total'], score['percentage']
        )

        self.bot.send_message(
            user_id, f'{text_message}\n\n{grade_message}'
        )

        self.bot.send_message(
            user_id,
            MESSAGES['ASK_TEACHER_REQUEST'],
            reply_markup=self.keyboard.request_teacher_markup()
        )

    @staticmethod
    def estimate_grade(percentage: int) -> str:
        for grade in config.QUIZ_GRADE_RANGE:
            boundaries = range(
                config.QUIZ_GRADE_RANGE[grade][0],
                config.QUIZ_GRADE_RANGE[grade][1] + 1
            )

            if percentage in boundaries:
                return grade

    def handle(self):

        @self.bot.poll_answer_handler()
        def handle(poll_answer):
            user = self.DB.get_user(user_id=poll_answer.user.id)

            if user is None or user.blocked:
                return

            self.poll_answer_received(poll_answer)
