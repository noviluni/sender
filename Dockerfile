FROM python:3.6-alpine

MAINTAINER Marc Hernandez "noviluni@gmail.com"

COPY . /src
WORKDIR /src
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["src/api.py"]