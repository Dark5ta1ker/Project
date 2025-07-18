FROM python:3.9-slim

WORKDIR /app

# Копируем сначала requirements.txt
COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Важно: Убедитесь что логи пишутся в stdout/stderr
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV FLASK_ENV=development

CMD ["python", "-m", "app.run"]
