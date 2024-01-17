# Dockerfile for the python discord bot

FROM python:3.11-alpine

WORKDIR /usr/src/chouettebot

COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python3","main.py"]
