FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY /app/cloud /app/cloud

EXPOSE 8080

CMD ["python", "/app/cloud/cloud_server.py"]