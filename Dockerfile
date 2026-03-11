FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install poetry
RUN pip install --no-cache-dir poetry==1.8.3

# Copy dependency files
COPY pyproject.toml poetry.toml ./

# Install dependencies (no dev group in production)
RUN poetry install --without dev --no-root

# Copy project
COPY . .

# Collect static files
RUN poetry run python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["poetry", "run", "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
