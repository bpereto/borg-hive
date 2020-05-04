FROM python:3.8-slim
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y libmariadbclient-dev python3-pip

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY src /app/
