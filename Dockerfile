# Dockerfile for the python discord bot

FROM python:3.12-alpine

WORKDIR /usr/src/chouettebot

COPY . .
RUN pip --no-cache-dir install -r requirements.txt

EXPOSE 8080
CMD ["python3", "main.py"]
