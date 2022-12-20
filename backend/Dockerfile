FROM python:3.9

ENV PYTHONUNBUFFERED=0

WORKDIR /srv/server
COPY . /srv/server

RUN    pip install --upgrade pip
RUN    pip install -r requirements.txt