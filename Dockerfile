FROM python:3.6-alpine
MAINTAINER Marc Hernandez "noviluni@gmail.com"

# Next line to compile postgresql binary
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev


ARG requirements=prod

COPY . /src
WORKDIR /src
RUN pip install -r requirements/$requirements.txt
CMD ["python", "src/run.py"]
