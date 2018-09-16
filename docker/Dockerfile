FROM python:3.6-alpine
RUN apk update && apk upgrade && pip install -U pip
RUN apk add --update gcc linux-headers py-pip musl-dev
# gunicorn on production configue it later
# RUN pip install gunicorn
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
# CMD ["gunicorn", "main:app", "-w 4", "-b 0.0.0.0:8000"]
CMD ["python", "main.py"]