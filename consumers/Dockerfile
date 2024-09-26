FROM python:3.12

WORKDIR /consumers
COPY . .
RUN pip install -r requirements.txt


CMD ["python", "process_order_consumer.py"]

