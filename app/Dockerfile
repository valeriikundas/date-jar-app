FROM python:3.12 AS build-stage
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
ENTRYPOINT ["gunicorn", "--workers", "4", "app:app", "--bind", "0.0.0.0:8000"]
