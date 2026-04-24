FROM python:3.12-slim

# Указываем Python не буферизировать логи (чтобы они сразу летели в docker logs)
ENV PYTHONUNBUFFERED=1

WORKDIR /app_testing

# 1. Создаем пользователя и папку для базы заранее
# Используем ID 1000 
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app_testing/db_folder && \
    chown -R appuser:appuser /app_testing

# 2. Ставим зависимости
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 3. Копируем код и сразу меняем владельца
COPY --chown=appuser:appuser . .

# 4. Переключаемся на пользователя
USER appuser

# Команда запуска (имя папки 'testing' берем из пути к wsgi.py)
CMD ["gunicorn", "--bind", "0.0.0.0:8001", "testing.wsgi:application"]








