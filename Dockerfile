FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

RUN apt update
RUN apt install -y pandoc

COPY ./app /app
WORKDIR /app
RUN pip install -r requirements.txt
