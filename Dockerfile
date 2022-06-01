FROM python:3.6-alpine

RUN apk add --no-cache chromium chromium-chromedriver

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENV DOWNLOAD_PATH=/app \
    BOISSIBOOK_API=http://boissibook:8080

EXPOSE 3000

CMD python app/app.py