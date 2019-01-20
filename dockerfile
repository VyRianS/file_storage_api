FROM python:3.6-alpine3.7
MAINTAINER "Jianyu Chen"
LABEL project="file_storage_api"
LABEL email="vyrians@gmail.com"

COPY . /usr/src/file-storage_api
WORKDIR /usr/src/file-storage_api

RUN pip install Flask

ENV FLASK_APP api.py
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
