# First, build the application in the `/usr/src/chouettebot` directory.
FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Omit development dependencies
ENV UV_NO_DEV=1

# Disable Python downloads, because we want to use the system interpreter across both images.
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /usr/src/chouettebot
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    if [ $(uname -m | cut -c 1-3) = "arm" ]; then \
    export UV_INDEX = https://www.piwheels.org/simple; fi \
    && uv sync --locked --no-install-project
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked


# Then, use a final image without uv
FROM python:3.13-alpine

# Setup a non-root user
RUN addgroup -S chouette -g 1000 \
 && adduser -S chouette -u 1000 -G chouette

# Copy the application from the builder
COPY --from=builder --chown=chouette:chouette /usr/src/chouettebot /usr/src/chouettebot

# Place executables in the environment at the front of the path
ENV PATH="/usr/src/chouettebot/.venv/bin:$PATH"

# Use the non-root user and move to the workdir
USER chouette
WORKDIR /usr/src/chouettebot

# Tell the bot that it's running inside a docker image
ENV DOCKER_RUNNING=true

# Permit to get the image tag inside of it (default version=local)
ARG version=local
ENV IMAGE_TAG=$version

EXPOSE 8080
CMD ["python3", "-m", "chouette"]
