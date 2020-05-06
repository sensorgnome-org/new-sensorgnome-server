# Sensorgnome-Server-Django

Development repo for the new Sensorgnome server, with a focus on extensibility, security and ease of development. Based on Django.

## Running the Project

Starting a development environment is simple:

- Install `docker` and `docker-compose`.
- Run `docker-compose build` to create the needed containers and images.
- Run `docker-compose up` to start the databse server, the message queue server and the Django worker processes.

## Django App Layout

The project is broken up into multiple parts:

- message_queue: this handles messages coming from the Sensorgnomes.
- rest_api: this handles tasks from the Sensorgnomes that are better handled over a REST API, rather than as message passing. Also handles registration and integration with Motus.org.
- sg_status: status pages for the Sensorgnomes.
- website: actual contents of the website.

## Project Layout

- Messaging: RabbitMQ server used to send and receive AMQP messages from the Sensorgnomes.
  - AMQP was chosen as it is similar to the existing messaging software Sensorgnomes already use, but adds encryption and authentication.
  - RabbitMQ was chosen as it is a full features message broker, allowing both sending and receiving of messages from a Sensorgnome, but also sending them to multiple endpoints. This could be used to support sending Sensorgnome data to more than one place, or send it to a non-Motus place.
- Django: Python based web-application framework, used for the user-facing and management parts of the server.
  - Django was chosen because it already supports a lot of the needed features out-of-the-box, including user and session management, and additionally has plugins for handling a lot of the additional features needed, such as Django Rest Framework for the REST API and integration with Celery for message processing.

## Project Goals

- Register and deploy new Sensorgnomes.
- Manage existing Sensorgnomes.
- View the status of new Sensorgnomes.
- Collect and manage data from Sensorgnomes.
- Troubleshoot problematic Sensorgnomes.
- Sync data and other information with Motus as needed.
