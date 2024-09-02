#Build
FROM python:3.12-bookworm AS builder

RUN pip install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_IN_PROJECT=1 \
  POETRY_VIRTUALENVS_CREATE=1 \
  POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

#Runtime
FROM python:3.12-slim-bookworm AS runtime

ENV VIRTUAL_ENV=/app/.venv \
  PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY food_chatbot ./food_chatbot

EXPOSE 7860

ENTRYPOINT ["python", "-m", "food_chatbot"]