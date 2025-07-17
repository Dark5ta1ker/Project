FROM python:3.9-slim

WORKDIR ./

# Копируем сначала requirements.txt
COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Важно: Убедитесь что логи пишутся в stdout/stderr
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]