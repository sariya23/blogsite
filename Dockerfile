FROM python:3.11.5-slim-bullseye

WORKDIR /code

COPY . /code
RUN pip install -r requirements.txt