FROM python:3.10

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "5001", "--backend-store-uri", "postgresql://postgres:postgres123@postgres-db:5432/postgres"]
