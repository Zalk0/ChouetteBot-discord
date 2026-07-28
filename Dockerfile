FROM python:3.13-alpine AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

ENV UV_LINK_MODE=copy
RUN if [ $(uname -m | cut -c 1-3) = "arm" ]; then \
    uv sync --no-dev --frozen \
    --extra-index-url https://www.piwheels.org/simple; else \
    uv sync --no-dev --frozen; fi

FROM python:3.13-alpine

RUN addgroup -S chouette -g 1000 \
    && adduser -S chouette -u 1000 -G chouette

WORKDIR /usr/src/chouettebot

COPY --from=builder /app/.venv .venv

COPY . .

ENV PATH="/usr/src/chouettebot/.venv/bin:$PATH"

USER chouette

ENV DOCKER_RUNNING=true

ARG version=local
ENV IMAGE_TAG=$version

EXPOSE 8080
CMD ["python3", "-m", "chouette"]
