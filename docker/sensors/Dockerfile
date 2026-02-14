FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY /app/sensors /app/sensors

ENV SENSOR_TYPE=north

CMD ["python", "/app/sensors/north.py"]