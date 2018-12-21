
# FROM ubuntu:latest
FROM python:3.6-alpine

MAINTAINER Marc Hernandez "noviluni@gmail.com"

# RUN apt-get update -y
# RUN apt-get install -y python-pip python-dev build-essential

COPY . /src
WORKDIR /src
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["src/api.py"]

