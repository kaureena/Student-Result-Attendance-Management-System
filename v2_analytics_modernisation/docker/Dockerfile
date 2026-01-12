# Template Dockerfile for API service
FROM python:3.11-slim

WORKDIR /app
COPY v2_analytics_modernisation/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000
CMD ["uvicorn", "v2_analytics_modernisation.api_service.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
