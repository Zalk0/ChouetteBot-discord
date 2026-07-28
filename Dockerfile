FROM python:3.13-alpine AS builder

RUN apk add --no-cache curl

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN source /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

COPY pyproject.toml uv.lock ./

ENV UV_LINK_MODE=copy
RUN uv sync --no-default-groups --frozen

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
