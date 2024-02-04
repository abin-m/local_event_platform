# Local Event Platform

The Local Event Platform is a dynamic and versatile web application designed to streamline event management for local communities. Whether you're organizing meetups, workshops, or social gatherings, this platform provides a centralized space to create, update, and manage events effortlessly.

# Key Features

- Event Creation: Easily create and publish events with details such as title, date, time, location, and description.

- Real-time Updates: Keep attendees informed with real-time updates for event modifications, cancellations, or additional information.

- User Authentication: Secure user authentication powered by Django's custom user model and token-based authentication using JWT.

- SMS Notifications: Enhance communication with attendees by sending SMS notifications using Twilio integration for important updates.

- Celery Integration: Utilizes Celery for handling asynchronous tasks, such as sending event notifications in the background.

- RESTful API: Built on Django REST framework, providing a robust and scalable API for seamless integration with other services.

- Redis for Message Broker: Utilizes Redis as a message broker for Celery to handle distributed task queue management.

- SQLite Database: A lightweight and easy-to-use SQLite database for storing application data.

# Technologies Used

- Django: A high-level Python web framework that encourages rapid development and clean, pragmatic design.

- Django REST Framework: A powerful and flexible toolkit for building Web APIs in Django.

- Celery: An asynchronous task queue/job queue based on distributed message passing.

- Twilio: A cloud communications platform for building SMS, Voice, and Messaging applications.

- JWT (JSON Web Tokens): A standard for securely transmitting information between parties as a JSON object.

- Redis: An open-source, in-memory data structure store used as a message broker for Celery.

- SQLite: A C library that provides a lightweight, disk-based database.
