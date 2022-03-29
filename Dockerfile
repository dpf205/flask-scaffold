FROM python:3.8-slim-buster

MAINTAINER David Francis <dpf205@gmail.com>

RUN apt-get update && apt-get install -qq -y build-essential libpq-dev --no-install-recommends
RUN apt-get -y install python-pip
RUN pip3 install --upgrade pip
RUN pip3 install psycopg2-binary
RUN pip install setuptools
RUN pip install --upgrade setuptools pip


ENV INSTALL_PATH /server_app
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .


CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "server_app.app:create_app()"
