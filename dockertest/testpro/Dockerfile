FROM python:3

RUN python -m pip install --upgrade pip

RUN apt-get update

WORKDIR /testpro

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /testpro/