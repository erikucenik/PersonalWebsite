FROM python:3.9

RUN apt update
RUN apt install -y pandoc

WORKDIR /code
COPY ./app/requirements.txt /code

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

WORKDIR /code/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]
