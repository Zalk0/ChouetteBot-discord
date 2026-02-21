FROM python:3.13-alpine

# Setup a non-root user and move to workdir
RUN addgroup -S chouette -g 1000 \
 && adduser -S chouette -u 1000 -G chouette
WORKDIR /usr/src/chouettebot

COPY pyproject.toml .
# If platform is arm then we add the piwheels index for prebuilt arm wheels
RUN if [ $(uname -m | cut -c 1-3) = "arm" ]; then \
    echo -e "[global]\nextra-index-url=https://www.piwheels.org/simple" > /usr/local/pip.conf; fi \
    && pip --no-cache-dir install -U pip \
    && pip --no-cache-dir install --only-binary=:all: . \
    && pip --no-cache-dir uninstall -y ChouetteBot && rm -rf *

COPY . .

# Use the non-root user
USER chouette

# Tell the bot that it's running inside a docker image
ENV DOCKER_RUNNING=true

# Permit to get the image tag inside of it (default version=local)
ARG version=local
ENV IMAGE_TAG=$version

EXPOSE 8080
CMD ["python3", "-m", "chouette"]
