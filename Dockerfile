# syntax=docker/dockerfile:1
FROM python:3

RUN apt-get update && \
 	apt-get upgrade -y && \
	apt-get install -y --no-install-recommends \
  graphviz \
  graphviz-dev && \
  apt-get -y clean && \
	apt-get -y autoclean && \
	apt-get -y autoremove

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/
