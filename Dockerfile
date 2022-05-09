FROM python:3.6-alpine

RUN apk update
RUN apk add chromium chromium-chromedriver

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

CMD python src/app.py