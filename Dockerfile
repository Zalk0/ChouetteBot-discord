FROM python:3.13-alpine AS builder

# Install uv from script + C toolchain to build packages without wheels for the target arch
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh \
    && apk add --no-cache build-base

ENV PATH="/root/.local/bin/:$PATH"

# Set uv environment to production
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEFAULT_GROUPS=1 \
    UV_NO_MANAGED_PYTHON=1

# Set workdir
WORKDIR /app

# Install requirements
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --locked --no-install-project

# Copy project files and compile bytecode of project files
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv run python -m compileall chouette/

FROM python:3.13-alpine

RUN addgroup -S chouette -g 1000 \
    && adduser -S chouette -u 1000 -G chouette

WORKDIR /home/chouette/app

COPY --from=builder /app .

ENV PATH="/home/chouette/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

USER chouette

ENV DOCKER_RUNNING=true

ARG version=local
ENV IMAGE_TAG=$version

EXPOSE 8080
CMD ["python3", "-m", "chouette"]
