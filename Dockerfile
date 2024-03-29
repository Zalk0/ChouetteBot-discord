# Dockerfile for the python discord bot
ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-alpine as build

WORKDIR /usr/src/chouettebot
COPY . .

RUN wget -O - https://sh.rustup.rs | sh -s -- -y && \
    PATH=$PATH:$HOME/.cargo/bin && \
    python3 -m venv venv  && venv/bin/pip --no-cache-dir install -r requirements.txt

FROM python:${PYTHON_VERSION}-alpine as prod

WORKDIR /usr/src/chouettebot
COPY --from=build /usr/src/chouettebot ./

EXPOSE 8080
CMD ["venv/bin/python3", "main.py"]
