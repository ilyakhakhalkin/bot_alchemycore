import os
from json import JSONEncoder

import pandas as pd
from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, scoped_session
# from data_base.dbcore import Base

from settings import config
# from models.quizzes import Quiz
# from models.questions import Question
# from models.answers import Answer
# from models.quiz_sessions import QuizSession
# from models.responses import Response
# from models.users import User

from .dbcore import Singleton
from .models.metadata import metadata
from .models.quizzes import quizzes
from .models.questions import questions
from .models.answers import answers
from .models.users import users
from .models.quiz_sessions import quiz_sessions
from .models.responses import responses


class DBManager(metaclass=Singleton):
    def __init__(self) -> None:
        print('DB:: Initializing DB manager')
        self.engine = create_engine(config.DATABASE)
        print('DB:: Engine created')
        # session = scoped_session(sessionmaker(bind=self.engine))
        # self._session = session()
        # print('DB:: Session created')

        self.metadata = metadata

        if not os.path.isfile(config.DATABASE):
            # Base.metadata.create_all(self.engine)
            self.metadata.create_all(self.engine)
            print('DB created')

    # def commit(self):
    #     print('DB:: Commiting DB changes')
    #     self._session.commit()

    # def close(self):
    #     print('DB:: Closing DB session')
    #     self._session.close()

    def retrieve_quizzes(self):
        print('DB:: retrieve_quizzes():')
        quizzes = self._session.query(Quiz).all()
        print('Retrieved' + str(quizzes))
        if len(quizzes) == 0:
            self.load_from_excel()
            quizzes = self._session.query(Quiz).all()

        return quizzes

    def user_lookup(self, user):
        print('DB:: user_lookup():')
        user_db = self._session.query(User).filter(User.id == user.id).scalar()
        print(f'User: {user_db}')
        if user_db is not None:
            print('User is already exists in DB')
            return

        user = User(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )

        print(f'New user: {user}')

        if user.username in config.DEFAULT_ADMINS:
            user.is_admin = 1

        self._session.add(user)
        self.commit()
        self.close()

    def new_quiz_session(self, user_id: int, quiz_id: int):
        print('DB:: new_quiz_session():')
        self.delete_redundant_quiz_sessions(user_id=user_id)

        quiz_session = QuizSession(user_id=user_id, quiz_id=quiz_id)
        print(f'New Quiz Session is {quiz_session}')

        self._session.add(quiz_session)
        self.commit()

        print('Next - populating session with responses')
        responses = self.populate_new_attempt(quiz_session=quiz_session)
        self.close()

        return responses

    def delete_redundant_quiz_sessions(self, user_id):
        print('DB:: delete_redundant_sessions')
        redundant = self._session.query(QuizSession).filter(
            QuizSession.user_id == user_id
        )

        for r in redundant:
            print(f'Del:: {r}')
            self._session.delete(r)

        self.commit()

    def populate_new_attempt(self, quiz_session):
        print('DB:: populate_new_attempt')
        for q in quiz_session.quiz.questions:
            resp = Response(question_id=q.id, quiz_session_id=quiz_session.id)
            print(f'New response:: {resp}')
            self._session.add(resp)

        self.commit()
        return quiz_session.responses

    def retrieve_response_object(self, user_id: int, poll_id: int = None):
        print('DB:: retrieve_response_object():')
        user = self._session.query(User).get(user_id)
        print(f'User object {user} is retrieved')
        print(f'Quiz session id: {user.quiz_sessions[0].id}')
        user_response = self._session.query(Response).filter(
            Response.quiz_session_id == user.quiz_sessions[0].id,
            # Response.poll_id == poll_id,
            # Response.answer == None
        ).first()
        print(f'{user_response} is user\'s response object')
        self.close()
        return user_response

    def register_new_poll(self, user_response, poll_id, options):
        print('DB:: register_new_poll')
        user_response.poll_id = int(poll_id)
        print(f'Poll_ID: {poll_id}')
        user_response.options = JSONEncoder().encode(o=options)
        print(f'Poll options: {user_response.options}')
        self.commit()
        self.close()

    def register_answer(self, user_response, answer_text):
        print('DB:: register_answer')
        print(f'answer text is {answer_text}')
        answer = user_response.question.answers.filter(Answer.text == answer_text).first()
        print(f'{answer} object retrieved')
        user_response.answer = answer
        print(f'{user_response} answer is set to {answer}')
        self.commit()
        self.close()

    def calculate_quiz_session_score(self, user_id):
        print('DB:: calculate_quiz_session_score')
        user = self._session.query(User).get(user_id)
        total = len(user.quiz_sessions[0].responses)
        score = 0

        for res in user.quiz_sessions[0].responses:
            if res.answer.is_correct:
                score += 1

        user.quiz_sessions[0].score = score

        self.commit()
        self.close()

        return total, score

    def mark_quiz_session_as_requested(self, user_id):
        print('DB:: mark_quiz_session_as_requested')
        user = self._session.query(User).get(user_id)
        user.quiz_sessions[0].requested = 1

        self.commit()
        self.close()

    def save_session_to_excel(self, user_id):
        print('DB:: save_session_to_excel')
        user = self._session.query(User).get(user_id)
        responses = user.quiz_sessions[0].responses

        data = []
        indexes = []

        for r in responses:
            if not r.answer:
                continue

            indexes.append(r.question.id)
            data.append([r.question.text, r.answer.text, r.answer.is_correct])

        df = pd.DataFrame(data, index=indexes, columns=['QUESTION', 'ANSWER', 'CORRECT'])
        filename = f'{user.username} {user.quiz_sessions[0].quiz.name}.xlsx'
        df.to_excel('requested_sessions/' + filename, sheet_name='new_sheet_name')

        self.close()

        return filename, user, user.quiz_sessions[0].date

    def grant_admin_permissions(self, requested_from, username):
        print('DB:: grant_admin_permissions')
        if not self._session.query(User).filter(User.id == requested_from).first().is_admin:
            return

        user = self._session.query(User).filter(User.username == username).first()
        if user:
            user.is_admin = 1

        self.commit()
        self.close()

    def remove_admin_permissions(self, requested_from, username):
        print('DB:: remove_admin_permissions')
        if not self._session.query(User).filter(User.id == requested_from).first().is_admin:
            return

        user = self._session.query(User).filter(User.username == username).first()
        if user:
            user.is_admin = 0

        self.commit()
        self.close()

    def get_admin_list(self):
        print('DB:: get_admin_list')
        admins = self._session.query(User).filter(User.is_admin == 1).all()
        print(f'Got {admins}')
        return [a.id for a in admins]

    def load_from_excel(self, filename='/quiz_data.xlsx'):
        print('DB:: load_data_from_excel')
        quizzes = self._session.query(Quiz).all()
        for q in quizzes:
            self._session.delete(q)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        df = pd.read_excel(BASE_DIR + filename)

        for row in df.itertuples():
            if row[0] == 0:
                continue

            quiz_name = row[1]
            quiz = self._session.query(Quiz).filter(Quiz.name == quiz_name).first()

            if quiz is None:
                quiz = Quiz(name=quiz_name)

            self._session.add(quiz)

            question = Question(text=row[2], quiz=quiz)
            self._session.add(question)

            answers = []

            for idx in range(3, len(row)):
                if str(row[idx]) not in ['', 'nan', '-', None, 'NULL']:
                    answers.append(
                        Answer(text=row[idx], question=question)
                    )
                    if idx == 3:
                        answers[-1].is_correct = True

            self._session.add_all(answers)
            self.commit()

        self.close()
