FROM python:3

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /

# Install dependencies.
RUN pip install -r /requirements.txt

# Set work directory.
RUN mkdir /src
WORKDIR /src

# Copy project code.
COPY . /src
WORKDIR /src/src/ucp

EXPOSE 8888
CMD python manage.py runserver 0.0.0.0:8888
