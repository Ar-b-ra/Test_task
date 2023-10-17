# Используем базовый образ Python
FROM python:latest
# Установка переменных среды
ENV HOST=localhost
ENV PORT=8000
# Установка зависимостей
RUN apt update -y && \
    apt upgrade -y && \
    apt install -y --no-install-recommends \
    python3-pip \
    python3-dev \
    python3-venv \
        git && \
    apt autoremove -y && \
    rm -rf /var/lib/apt/lists/*
# Копирование файлов в рабочую директорию
COPY . /Test_task
# Установка рабочей директории
WORKDIR /Test_task
# Установка зависимостей
RUN apt install -y python3-pip && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt
# Запуск приложения
EXPOSE 8000
EXPOSE 5432
CMD ["python3", "main.py"]