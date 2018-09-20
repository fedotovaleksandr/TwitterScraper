FROM python:3.6-alpine
RUN apk update && apk upgrade && pip install -U pip
RUN apk add --update gcc linux-headers py-pip musl-dev libxml2-dev libxslt-dev python-dev
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["gunicorn", "main:app","--reload", "-w 4", "-b 0.0.0.0:9090"]