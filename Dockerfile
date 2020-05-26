FROM python:3.8.2-buster

ENV PYTHONUNBUFFERED 1

# Copy requirements Pipfile from local to container
COPY ./Pipfile /Pipfile
COPY ./Pipfile.lock /Pipfile.lock

RUN apt-get update && apt-get install -y ca-certificates postgresql-client netcat
# Install Geodjango dependencies
RUN apt-get install -y binutils libproj-dev gdal-bin
RUN pip install pipenv
RUN pipenv install --system --deploy

# Copy and set our project folder from local to container
RUN mkdir /sensorgnome-server-software
WORKDIR /sensorgnome-server-software
COPY ./ /sensorgnome-server-software

# Copy the wait-for script from local to container
COPY ./wait-for /bin/wait-for
RUN chmod 777 -R /bin/wait-for
RUN useradd user
USER user