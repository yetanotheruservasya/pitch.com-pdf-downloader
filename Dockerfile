# Используем базовый образ с Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости с очисткой кэша apt и pip
RUN apt-get update && \
    apt-get install -y \
    libnss3 \
    libgconf-2-4 \
    libxss1 \
    libasound2 \
    libx11-6 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libexpat1 \
    libxcb1 \
    libxkbcommon0 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libatspi2.0-0

# Очистка кэша apt
RUN rm -rf /var/lib/apt/lists/*

# Установка зависимостей Python и Selenium
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install selenium webdriver-manager

# Очистка кэша pip и Playwright
RUN rm -rf /root/.cache/*

# Открываем порт для приложения
EXPOSE 5007

# Команда для запуска приложения
CMD ["python", "pitch2pdf_service.py"]
