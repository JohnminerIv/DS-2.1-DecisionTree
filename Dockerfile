FROM python:3.7-slim-buster

ADD requirements.txt /app

RUN python3 -m pip install -r /app/requirements.txt

ADD . /app

WORKDIR /app

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "app"]