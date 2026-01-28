FROM python:3.13-alpine3.22 AS base

WORKDIR /workspace
# copy installation files
COPY pyproject.toml .

USER root

RUN apk add curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh

# adding uv to PATH
ENV PATH="/root/.local/bin:${PATH}"

RUN uv sync --extra api

# copy service files
COPY api/src /workspace/src/

WORKDIR /workspace/src

ENTRYPOINT ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
