ARG IMAGE=python:3.8-buster
FROM ${IMAGE}

ENV PATH "/home/.local/bin/:${PATH}"

RUN pip install --upgrade pip wheel setuptools

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt -r requirements-test.txt
RUN pip install -e .
