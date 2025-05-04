FROM python:3.12-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    python3-dev \
    libffi-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Копирование pyproject.toml вместо requirements.txt
COPY pyproject.toml .

# Установка зависимостей через poetry (без poetry.lock)
RUN poetry config virtualenvs.create false && \
    poetry install --no-root

# Создание непривилегированного пользователя
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Установка PYTHONPATH
ENV PYTHONPATH=/app

CMD ["uvicorn", "app.src.main:app", "--host", "]()
