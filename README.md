# Boissibook-scraper

## Start project without docker

- you need to have chromedriver install on your system

- create a virtualenv

- start it

- install dependensies -> `pip install -r requirements.txt`

- add .env with your download folder path 

- start project

```
python src/app.py
```

## Start project with docker

- add .env with the docker download folder

- run the command below

```
docker compose up --build
```