FROM python:3.10-slim

RUN apt-get update && apt-get install -y git && apt-get clean


COPY requirements.txt /app/.

WORKDIR /app

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python", "app.py"]

