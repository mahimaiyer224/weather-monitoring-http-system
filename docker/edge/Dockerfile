FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY /app/edge /app/edge

ENV EDGE_TYPE=ne

CMD ["python", "/app/edge/ne_edge.py"]