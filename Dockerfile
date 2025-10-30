# Stage 1: Base image with Playwright
FROM python:3.13.9-slim-bookworm AS playwright-base

RUN pip install playwright && playwright install --with-deps

# Stage 2: Application build
FROM playwright-base AS app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

RUN mkdir secrets

COPY pyproject.toml uv.lock ./

RUN uv sync --locked

COPY ./src .

CMD ["uv", "run", "main.py"]