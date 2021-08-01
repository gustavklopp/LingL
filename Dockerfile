# You need first to start docker daemon: sudo dockerd

# Base Image
FROM python:3.9.0

# create and set working directory
RUN mkdir /app
WORKDIR /app
COPY requirements_SERVERONLY.txt /app/

# Add current directory code to working directory
ADD . /app/

# set default environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive 

# set project environment variables
# grab these via Python's os.environ
# these are 100% optional here
ENV PORT=8000

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
        python3-setuptools \
        python3-pip \
        python3-dev \
        python3-venv \
        git \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install pyenv:
ENV HOME="/root"
WORKDIR ${HOME}
RUN git clone --depth=1 https://github.com/pyenv/pyenv.git .pyenv
ENV PYENV_ROOT="${HOME}/.pyenv"
ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:${PATH}"

ENV PYTHON_VERSION=3.9.0
RUN pyenv install ${PYTHON_VERSION}
RUN pyenv global ${PYTHON_VERSION}

RUN pip3 install --upgrade pip 

# Install project dependencies
WORKDIR /app
RUN pip3 install -r requirements_SERVERONLY.txt

EXPOSE 8000
STOPSIGNAL SIGTERM
CMD gunicorn LingL.wsgi:application --bind 0.0.0.0:$PORT
