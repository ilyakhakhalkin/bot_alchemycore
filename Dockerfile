FROM python:3.7.6-buster

WORKDIR /sprachbot_alchemy
COPY . .

RUN apt-get update \
    && apt-get -y install libpq-dev gcc
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt --no-cache-dir