FROM python:3.8-slim
MAINTAINER bpereto

# set environment variables
ENV PYTHONDONTWRITEBYTE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y libmariadbclient-dev python3-pip libsasl2-dev python-dev libldap2-dev libssl-dev

RUN mkdir /app /staticfiles && groupadd -g 1000 borg && \
    useradd -rm -u 1000 -g 1000 borg && chown -R borg:borg /app /staticfiles
WORKDIR /app
COPY requirements.txt /app/

RUN pip install --no-cache -r requirements.txt

# install uwsgi now because it takes a little while
RUN pip3 install --no-cache uwsgi

COPY src /app/
COPY scripts/init.sh /
COPY uwsgi.ini /

VOLUME ["/staticfiles"]

USER borg

ENTRYPOINT ["/init.sh"]
