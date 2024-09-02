# Build stage
FROM python:3.12-bookworm AS python-dev

RUN pip install poetry==1.8.3

WORKDIR /app

ENV POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_IN_PROJECT=1 \
  POETRY_VIRTUALENVS_CREATE=1 \
  POETRY_CACHE_DIR=/tmp/poetry_cache

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

# Runtime stage
FROM python:3.12-slim-bookworm AS runtime

COPY --from=python-dev /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

COPY . /app

WORKDIR /app

EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"

CMD ["python", "-m", "food_chatbot.__main__"]