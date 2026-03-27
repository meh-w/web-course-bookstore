FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=bookstore.settings

RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    python3-dev \
    build-essential \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements/ /app/requirements/

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements/prod.txt

COPY . .

RUN mkdir -p staticfiles media
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "bookstore.wsgi:application", "--bind", "0.0.0.0:8000"]