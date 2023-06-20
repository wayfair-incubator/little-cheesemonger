ARG IMAGE=python:3.11-buster
FROM ${IMAGE}

# Set up user for automatic git branch creation
ARG _USER="little-cheesemonger"
ARG _UID="1001"
ARG _GID="100"
ARG _SHELL="/bin/bash"
RUN useradd -m -s "${_SHELL}" -N -u "${_UID}" "${_USER}"
ENV USER ${_USER}
ENV UID ${_UID}
ENV GID ${_GID}
ENV HOME /home/${_USER}
ENV PATH "${HOME}/.local/bin/:${PATH}"

RUN pip install --upgrade pip wheel setuptools

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt -r requirements-test.txt
RUN pip install -e .
