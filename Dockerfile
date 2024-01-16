# Dockerfile for the python discord bot

FROM python:3.12-alpine             # test with 3.11-alpine if gcc needed or not

RUN apk --no-cache add gcc musl-dev

WORKDIR /usr/src/chouettebot

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["python3","main.py"]
