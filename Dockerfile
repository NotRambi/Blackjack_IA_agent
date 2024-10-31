FROM ubuntu:latest

WORKDIR /app

RUN apt-get update \
 && apt-get install --assume-yes --no-install-recommends --quiet \
        python3 \
        python3-pip \
	python3-tk \
 && apt-get clean all

COPY . .

RUN pip3 install -r requirements.txt

