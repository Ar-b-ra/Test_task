# Используем базовый образ Python
FROM python:3.9-slim-buster

# Установка переменных среды
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Установка зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        postgresql-client \
        gcc \
        python3-dev \
        libpq-dev \
        netcat && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Создание директории приложения
RUN mkdir /app

# Установка рабочей директории
WORKDIR /app

# Копирование файлов в рабочую директорию
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копирование кода приложения в рабочую директорию
COPY . /app/

# Запуск PostgreSQL и создание базы данных
RUN service postgresql start && \
    su - postgres -c "psql -c 'CREATE DATABASE test_db;'"

# Запуск приложения
CMD ["python", "wsgi.py"]