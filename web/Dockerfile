FROM ubuntu:latest
MAINTAINER Răzvan Țiu "razvan_tiu@yahoo.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /web
WORKDIR /web
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["webserver.py"]
