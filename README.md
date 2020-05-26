# Sensorgnome-Server-Django

Development repo for the new Sensorgnome server, with a focus on extensibility, security and ease of development. Based on Django.

## Running the Project

Starting a development environment is simple:

- Install `docker` and `docker-compose`.
- Run `docker-compose build` to create the needed containers and images.
- Run `docker-compose up` to start the databse server, the message queue server, Django and the worker processes.

Note that the current set up does not support production usage.

## Django App Layout

The project is broken up into multiple parts:

- message_queue: this handles messages coming from the Sensorgnomes.
- rest_api: this handles tasks from the Sensorgnomes that are better handled over a REST API, rather than as message passing. Also handles registration and integration with Motus.org.
- sg_status: status pages for the Sensorgnomes.
- website: actual contents of the website.

## Project Layout & Rationale

- Messaging: RabbitMQ server used to send and receive AMQP messages from the Sensorgnomes.
  - AMQP was chosen as it is similar to the existing messaging software Sensorgnomes already use, but adds encryption and authentication. It is also better suited to low-bandwidth, high-latency, low-reliability connections in ways that using an HTTP based API is poorly suited to. Additionally, having a SensorGnome listen to a queue allows us to push commands to a SensorGnome directly, for maintenance or management.
  - RabbitMQ was chosen as it is a full featured message broker, allowing both sending and receiving of messages from a Sensorgnome, but also sending them to multiple endpoints. This could be used to support sending Sensorgnome data to more than one place, or send it to a non-Motus place.
- Django: Python based web-application framework, used for the user-facing and management parts of the server.
  - Django was chosen because it already supports a lot of the needed features out-of-the-box, including user and session management, and additionally has plugins for handling a lot of the additional features needed, such as Django Rest Framework for the REST API and integration with Celery for message processing.
- Celery: Celery is designed as a work queue system, to enable long-running tasks to be processed asynchronously in the background without stalling out other tasks. It uses AMQP and RabbitMQ to do IPC between the orchestrator and workers.
  - Where does Celery come in to play with the project, as there's not really any work like this? Django's event model is limited to getting called when a view is called, and that really only supports HTTP communication. However, Celery allows messages to be added to the queue from external processes, and then the workers can process these messages. This functionality is used to receive messages sent from SensorGnomes and then processed by Django based worker.

## Project Goals

- Register and deploy new Sensorgnomes.
- Manage existing Sensorgnomes.
- View the status of Sensorgnomes.
  - Receive alerts based on status events.
- Collect and manage data from Sensorgnomes.
- Troubleshoot problematic Sensorgnomes.
- Sync data and other information with Motus as needed.
