FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

RUN apt update
RUN apt install -y pandoc

COPY ./app /app
