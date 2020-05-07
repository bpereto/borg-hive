FROM python:3.8-slim
MAINTAINER bpereto

# set environment variables
ENV PYTHONDONTWRITEBYTE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y libmariadbclient-dev python3-pip

RUN mkdir /app /static && useradd -rm -u 1000 borg && chown -R borg:borg /app /static
WORKDIR /app
COPY requirements.txt /app/

RUN pip install --no-cache -r requirements.txt

# install uwsgi now because it takes a little while
RUN pip3 install --no-cache uwsgi

COPY src /app/
COPY scripts/init.sh /
COPY uwsgi.ini /

VOLUME ["/static"]

USER borg

ENTRYPOINT ["/init.sh"]
