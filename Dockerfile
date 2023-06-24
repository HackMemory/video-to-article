# Используем базовый образ Python
FROM python:3.9

# Установка переменной окружения для запуска в режиме совместимости
ENV PYTHONUNBUFFERED 1

# Копирование зависимостей в контейнер
COPY ./requirements.txt /requirements.txt

# Установка зависимостей Python
RUN --mount=type=cache,target=/root/.cache/pip pip install -r /requirements.txt

# Создание директории приложения в контейнере
RUN mkdir /app

# Установка рабочей директории
WORKDIR /app

# Копирование кода приложения в контейнер
COPY ./app /app