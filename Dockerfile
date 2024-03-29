# Dockerfile for the python discord bot

FROM python:3.11-alpine

WORKDIR /usr/src/chouettebot

COPY . .
RUN echo -e "[global]\nextra-index-url=https://www.piwheels.org/simple" >> /usr/local/pip.conf && \
    pip --no-cache-dir install -r requirements.txt

EXPOSE 8080
CMD ["python3", "main.py"]
