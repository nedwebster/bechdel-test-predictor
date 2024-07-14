FROM python:3.10

WORKDIR /app

COPY requirements.txt host_mlflow.sh /app/

RUN pip install -r requirements.txt

CMD ["sh", "host_mlflow.sh"]
