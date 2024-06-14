FROM python:3.12-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 8080/tcp
CMD ["python3", "service1.py"]