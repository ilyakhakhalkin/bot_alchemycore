import os
from pathlib import Path
from typing import List

import pandas as pd
from sqlalchemy import create_engine, insert, select, delete, and_, or_, update
from sqlalchemy.sql.expression import true, false
from sqlalchemy.sql import func, desc

from settings import config

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

        self.engine = create_engine(config.DATABASE, echo=True)
        self.metadata = metadata

        if not os.path.isfile(config.DATABASE):
            self.metadata.create_all(self.engine)

        self.connection = self.engine.connect()

    def get_user(self, user_id: int = None, username: str = None):
        s = select(users)

        if username is not None:
            s = s.where(users.c.username == username)

        if user_id is not None:
            s = s.where(users.c.id == user_id)

        return self.connection.execute(s).first()

    def get_user_count(self):
        s = select(func.count()).select_from(users)
        return self.connection.execute(s).first()[0]

    def create_user(
        self,
        user_data=None,
        id: int = None,
        username: str = None,
        first_name: str = None,
        last_name: str = None,
        full_name: str = None,
        is_admin: bool = False,
        blocked: bool = False,
    ):
        data = [
            {
                'id': getattr(user_data, 'id', id),
                'username': getattr(user_data, 'username', username),
                'first_name': getattr(user_data, 'first_name', first_name),
                'last_name': getattr(user_data, 'last_name', last_name),
                'full_name': getattr(user_data, 'full_name', full_name),
                'is_admin': getattr(user_data, 'is_admin', is_admin),
                'blocked': getattr(user_data, 'blocked', blocked),
            }
        ]

        if (str(data[0]['id']) in config.DEFAULT_ADMINS):
            data[0]['is_admin'] = True

        ins = users.insert()
        rp = self.connection.execute(ins, data)
        self.connection.commit()

        return self.get_user(user_id=rp.inserted_primary_key[0])

    def update_user(self, user_data):
        data = {
                'username': getattr(user_data, 'username'),
                'first_name': getattr(user_data, 'first_name'),
                'last_name': getattr(user_data, 'last_name'),
                'full_name': getattr(user_data, 'full_name'),
            }

        u = update(users).where(users.c.id == user_data.id)
        u = u.values(data)
        self.connection.execute(u)
        self.connection.commit()

    def block_user(self, user_id):
        u = update(users).where(users.c.id == user_id)
        u = u.values(blocked=True)
        self.connection.execute(u)
        self.connection.commit()

    def unblock_user(self, user_id):
        u = update(users).where(users.c.id == user_id)
        u = u.values(blocked=False)
        self.connection.execute(u)
        self.connection.commit()

    def get_quizzes(self, id: int = None, name: str = None):
        s = select(quizzes)

        if id is not None:
            s = s.where(quizzes.c.id == id)
            return self.connection.execute(s).first()

        if name is not None:
            s = s.where(quizzes.c.name == name)
            return self.connection.execute(s).first()

        return self.connection.execute(s).fetchall()

    def get_questions(self, quiz_id: int = None, q_id: int = None):
        if q_id is not None:
            s = select(questions).where(questions.c.id == q_id).limit(1)
            return self.connection.execute(s).first()

        s = select(questions).where(questions.c.quiz_id == quiz_id)
        return self.connection.execute(s).fetchall()

    def get_answers(
        self,
        q_id_list: List[int] = None,
        ans_id: int = None,
        text: str = None,
        correct_only: bool = False
    ):
        s = select(answers)
        print(q_id_list, ' is qquestion id list')

        if ans_id is not None:
            s = s.where(answers.c.id == ans_id).limit(1)
            return self.connection.execute(s).first()

        if text is not None:
            s = s.where(answers.c.text == text)

        if correct_only:
            s = s.where(answers.c.is_correct == true())

        if q_id_list is not None:
            s = s.where(answers.c.question_id.in_(q_id_list))

        return self.connection.execute(s).fetchall()

    def get_quiz_session(self, user_id):
        s = select(quiz_sessions).where(
            quiz_sessions.c.user_id == user_id,
            quiz_sessions.c.completed == false()
        ).order_by(desc(quiz_sessions.c.date))

        return self.connection.execute(s).first()

    def get_responses(self, user_id: int = None, qsession_id: int = None):
        s = select(responses)

        if user_id is not None:
            s = s.where(responses.c.user_id == user_id)

        if qsession_id is not None:
            s = s.where(responses.c.quiz_session_id == qsession_id)

        return self.connection.execute(s).fetchall()

    def create_quiz(self, name: str):
        ins = insert(quizzes).values(name=name)
        rp = self.connection.execute(ins)
        self.connection.commit()

        return rp.inserted_primary_key

    def create_question(self, text: str, quiz_id: int):
        ins = insert(questions).values(text=text, quiz_id=quiz_id)
        rp = self.connection.execute(ins)
        self.connection.commit()

        return rp.inserted_primary_key

    def create_answer(self, text: str = None, q_id: int = None, data=None):
        ins = insert(answers)

        if data is not None:
            self.connection.execute(ins, data)
            self.connection.commit()
            return

        ins = ins.values(text=text, question_id=q_id)
        self.connection.execute(ins)
        self.connection.commit()

    def create_quiz_session(self, user_id: int, quiz_id: int):
        ins = insert(quiz_sessions).values(
            user_id=user_id,
            quiz_id=quiz_id,
        )

        rp = self.connection.execute(ins)
        self.connection.commit()

        return rp.inserted_primary_key[0]

    def delete_quiz_sessions(self, user_id):
        d = delete(quiz_sessions).where(
            quiz_sessions.c.user_id == user_id,
            quiz_sessions.c.completed == false(),
        )
        self.connection.execute(d)
        self.connection.commit()

    def delete_responses(self, user_id: int):
        d_responses = delete(responses).where(responses.c.user_id == user_id)
        self.connection.execute(d_responses)
        self.connection.commit()

    def create_response(self,
                        data: List[dict] = None,
                        qsession_id: int = None,
                        q_id: int = None,
                        user_id: int = None,
                        ans_id: int = None,
                        options: str = None,
                        poll_id: int = None
                        ):
        if data is not None:
            ins = responses.insert()
            self.connection.execute(ins, data)
            self.connection.commit()
            return

        ins = insert(responses).values(
            qsession_id=qsession_id,
            q_id=q_id,
            ans_id=ans_id,
            options=options,
            poll_id=poll_id
        )

        rp = self.connection.execute(ins)
        self.connection.commit()

        return rp.inserted_primary_key

    def new_quiz_session(self, user_id: int, quiz_id: int):
        self.delete_responses(user_id)
        self.delete_quiz_sessions(user_id)

        qsession_id = self.create_quiz_session(
            user_id=user_id,
            quiz_id=quiz_id
        )
        q_list = self.get_questions(quiz_id)

        responses_data = [{
                'quiz_session_id': qsession_id,
                'question_id': q.id,
                'user_id': user_id,
            }
            for q in q_list
        ]

        self.create_response(data=responses_data)

        return len(q_list)

    def get_next_response(self, user_id):
        qsession = self.get_quiz_session(user_id=user_id)

        s = select(responses).where(
            and_(
                responses.c.quiz_session_id == qsession.id,
                responses.c.poll_id == None
            )
        )

        return self.connection.execute(s).first()

    def get_current_response(self, user_id: int, poll_id: int):
        qsession = self.get_quiz_session(user_id=user_id)

        s = select(responses).where(
            and_(
                responses.c.poll_id == poll_id,
                responses.c.quiz_session_id == qsession.id,
            )
        ).limit(1)

        return self.connection.execute(s).first()

    def update_response(self,
                        response_id: int,
                        poll_id: int = None,
                        options: str = None,
                        answer_id: int = None,
                        ):

        upd = update(responses)

        if poll_id is not None and options is not None:
            upd = upd.where(
                responses.c.id == response_id).values(
                    poll_id=poll_id,
                    options=options
                )

        if answer_id is not None:
            upd = upd.where(
                responses.c.id == response_id).values(answer_id=answer_id)

        self.connection.execute(upd)
        self.connection.commit()

    def get_score(self, qsession):
        q = self.get_questions(quiz_id=qsession.quiz_id)

        correct_ans = self.get_answers(
            q_id_list=[_.id for _ in q],
            correct_only=True
        )

        corr_ans_id = [ans.id for ans in correct_ans]
        s = select(responses).where(responses.c.quiz_session_id == qsession.id)
        rp = self.connection.execute(s).fetchall()

        score = {
            'total': len(rp) if len(rp) > 0 else 30,
            'points': 0,
        }

        for res in rp:
            if res.answer_id in corr_ans_id:
                score['points'] += 1

        score['percentage'] = int((score['points'] / score['total']) * 100)

        return score

    def request_session(self, user_id):
        u = select(quiz_sessions).where(
            quiz_sessions.c.user_id == user_id,
            quiz_sessions.c.completed == true(),
            quiz_sessions.c.requested == false(),
        ).order_by(desc(quiz_sessions.c.date))

        qsession = self.connection.execute(u).first()
        if qsession:
            self.update_qsession(qsession=qsession, requested=True)

        return qsession

    def update_qsession(self,
                        qsession,
                        filepath: str = None,
                        score: int = None,
                        completed: bool = False,
                        requested: bool = False,
                        ):
        u = update(quiz_sessions).where(quiz_sessions.c.id == qsession.id)

        if requested:
            u = u.values(requested=requested)
        if filepath:
            u = u.values(filepath=filepath)
        if score:
            u = u.values(score=score)
        if completed:
            u = u.values(completed=completed)

        self.connection.execute(u)
        self.connection.commit()

    def get_admins(self):
        s = select(users).where(
            or_(
                users.c.is_admin == true(),
                users.c.username.in_(
                    [admin for admin in config.DEFAULT_ADMINS]
                )
            )
        )
        return self.connection.execute(s).fetchall()

    def export_session(self, user):
        qsession = self.get_quiz_session(user.id)

        if qsession is None:
            return None, None

        quiz = self.get_quizzes(id=qsession.quiz_id)
        user_responses = self.get_responses(qsession_id=qsession.id)

        data = []
        indexes = []

        for i, r in enumerate(user_responses):
            ans = self.get_answers(ans_id=r.answer_id)
            q = self.get_questions(q_id=r.question_id)

            indexes.append(i + 1)
            data.append(
                [
                    getattr(q, 'text', 'Question not found'),
                    getattr(ans, 'text', ''),
                    config.ANSWER_LABELS[getattr(ans, 'is_correct', None)]
                ]
            )

        df = pd.DataFrame(
            data,
            index=indexes,
            columns=['Q', 'A', '+/-']
        )

        styled = (
            df.style.applymap(
                lambda v: config.ANSWER_COLORS[v] if v in config.ANSWER_COLORS else ''
            )
        )
        styled.apply(color, axis=1)

        filename = f'{user.full_name}_{quiz.name}.xlsx'
        dirname = os.path.join(
            config.BASE_DIR,
            config.EXCEL_FOLDER,
            'users',
            str(user.id),
            str(qsession.id)
        )

        fullpath = os.path.join(dirname, filename)

        if not os.path.isdir(dirname):
            Path(dirname).mkdir(parents=True)

        styled.to_excel(fullpath, engine='openpyxl')

        return fullpath

    def import_data(
        self,
        path=os.path.join(
            config.BASE_DIR, config.EXCEL_FOLDER, 'quiz_data.xlsx'
        )
    ):
        self.connection.execute(delete(answers))
        self.connection.execute(delete(questions))
        self.connection.execute(delete(quizzes))
        self.connection.execute(delete(responses))
        self.connection.execute(delete(quiz_sessions))
        self.connection.commit()

        df = pd.read_excel(path)

        added_quizzes = set()

        for row in df.itertuples():
            if row[0] == 0:
                continue

            if row[1] not in added_quizzes:
                self.create_quiz(row[1])
                added_quizzes.add(row[1])

            quiz = self.get_quizzes(name=row[1])

            question_id = self.create_question(quiz_id=quiz.id, text=row[2])[0]
            answers_data = []
            dub_checker = []

            for idx in range(3, len(row)):
                text = str(row[idx]).strip()
                if text in ['', 'nan', '-', None, 'NULL', 'None']:
                    continue

                if text in dub_checker:
                    text += 'er'

                is_correct = 1 if idx == 3 else 0
                answers_data.append(
                    {
                        'question_id': question_id,
                        'text': text,
                        'is_correct': is_correct
                    }
                )

                dub_checker.append(text)

            self.create_answer(data=answers_data)


def color(row):
    if row[2] is True:
        return ['background-color: lightgreen'] * len(row)
    elif row[2] is False:
        return ['background-color: #FF7777'] * len(row)
    return [''] * len(row)
