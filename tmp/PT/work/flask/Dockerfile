# pull official base image
FROM python:3.10-alpine3.17


# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1


# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1


# set work directory
WORKDIR /flask_app


# update the system and add git
RUN apk update
RUN apk add git


# install dependencies
COPY ./requirements.txt /flask_app
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install --upgrade pip
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt


# copy project
COPY . /flask_app


# specify the entry point
RUN chown -R 1000 /flask_app/
RUN chmod 755 /flask_app/gunicorn_starter.sh
ENTRYPOINT [ "./gunicorn_starter.sh" ]


# keep the Docker process running even when crashes
CMD ["tail", "-f", "/dev/null"]
