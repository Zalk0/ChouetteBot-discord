# Dockerfile for the python discord bot
FROM python:3.11-alpine

WORKDIR /usr/src/chouettebot

COPY requirements.txt .
# If platform is arm then we add the piwheels index for prebuilt arm wheels
RUN if [ $(uname -m | cut -c 1-3) = "arm" ]; then \
    echo -e "[global]\nextra-index-url=https://www.piwheels.org/simple" > /usr/local/pip.conf; fi && \
    pip --no-cache-dir install -r requirements.txt

COPY . .

# Tell the bot that it's running inside a docker image
ENV DOCKER_RUNNING=true

# Permit to get the image tag inside it
# build the image with `docker build  --build-arg tag="tag" -t app:tag`
ARG tag
ENV IMAGE_TAG=$tag

EXPOSE 8080
CMD ["python3", "main.py"]
