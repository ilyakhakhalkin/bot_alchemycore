FROM python:3.7-slim

WORKDIR /sprachbot_alchemy

COPY . .

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip3 install psycopg2

RUN pip3 install --upgrade pip && pip install -r requirements.txt --no-cache-dir

CMD python3 tgbot.py