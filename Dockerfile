FROM python:3.11.5-slim-bullseye

WORKDIR /code

COPY . /code
EXPOSE 8000
RUN pip install -r requirements.txt