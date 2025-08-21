FROM python:3.9-slim

WORKDIR /app

# Копируем сначала requirements.txt
COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Копируем ВСЁ содержимое проекта (включая app/)
COPY . .

# Изменяем команду запуска
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
