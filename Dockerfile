# Используем официальный slim-образ Python 3.12
FROM python:3.12-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \\\\
    gcc \\\\
    libpq-dev \\\\
    && apt-get clean \\\\
    && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей в контейнер
COPY pyproject.toml ./

# Устанавливаем зависимости Python
RUN poetry config virtualenvs.create false && \
    poetry install --no-root

# Копируем исходный код приложения в контейнер
COPY . .

# Создаем директорию для медиафайлов
RUN mkdir -p /config/media

# Пробрасываем порт, который будет использовать Django
EXPOSE 8000

# Команда для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]