FROM python:3.13.9-slim-bookworm 

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --locked

COPY ./src .

CMD ["uv", "run", "main.py"]
