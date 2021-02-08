ARG IMAGE_TAG=3.8-buster
FROM python:${IMAGE_TAG}

RUN pip install --upgrade pip wheel setuptools

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt -r requirements-test.txt
RUN pip install -e .
