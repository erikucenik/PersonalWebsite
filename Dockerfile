#FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

FROM python:3.9

RUN apt update
RUN apt install -y pandoc

WORKDIR /code
COPY ./app /code/app

WORKDIR /code/app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]



#COPY ./requirements.txt /code/requirements.txt

#RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#COPY ./app /code/app

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
#

###

#RUN apt update
#RUN apt install -y pandoc

#COPY ./app /app
#WORKDIR /app
#RUN pip install -r requirements.txt
