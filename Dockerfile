# Dockerfile for the python discord bot
FROM python:3.11-alpine

WORKDIR /usr/src/chouettebot

COPY requirements.txt .
# If platform is arm then we add the piwheels index for prebuilt wheels
RUN if [ $(uname -m | cut -c 1-3) = "arm" ]; then \
    echo -e "[global]\nextra-index-url=https://www.piwheels.org/simple" > /usr/local/pip.conf; fi && \
    pip --no-cache-dir install -r requirements.txt

COPY . .

EXPOSE 8080
CMD ["python3", "main.py"]
