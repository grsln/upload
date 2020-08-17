FROM python:3.7.8-alpine3.12

# set work directory
WORKDIR /usr/src/up_site

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apk update \
    && apk add gcc python3-dev musl-dev

# install pillow dependencies
RUN apk add jpeg-dev zlib-dev libjpeg

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install wheel
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .

# copy project
COPY . .

# run entrypoint.sh
#ENTRYPOINT ["/usr/src/up_site/entrypoint.sh"]
