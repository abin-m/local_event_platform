# Local Event Platform

The Local Event Platform is a dynamic and versatile web application designed to streamline event management for local communities. Whether you're organizing meetups, workshops, or social gatherings, this platform provides a centralized space to create, update, and manage events effortlessly.

## Key Features

- Event Creation: Easily create and publish events with details such as title, date, time, location, and description.

- Real-time Updates: Keep attendees informed with real-time updates for event modifications, cancellations, or additional information.

- User Authentication: Secure user authentication powered by Django's custom user model and token-based authentication using JWT.

- SMS Notifications: Enhance communication with attendees by sending SMS notifications using Twilio integration for important updates.

- Celery Integration: Utilizes Celery for handling asynchronous tasks, such as sending event notifications in the background.

- RESTful API: Built on Django REST framework, providing a robust and scalable API for seamless integration with other services.

- Redis for Message Broker: Utilizes Redis as a message broker for Celery to handle distributed task queue management.

- SQLite Database: A lightweight and easy-to-use SQLite database for storing application data.

## Technologies Used

- Django: A high-level Python web framework that encourages rapid development and clean, pragmatic design.

- Django REST Framework: A powerful and flexible toolkit for building Web APIs in Django.

- Celery: An asynchronous task queue/job queue based on distributed message passing.

- Twilio: A cloud communications platform for building SMS, Voice, and Messaging applications.

- JWT (JSON Web Tokens): A standard for securely transmitting information between parties as a JSON object.

- Redis: An open-source, in-memory data structure store used as a message broker for Celery.

- SQLite: A C library that provides a lightweight, disk-based database.

## Installation

clone the repo and install the required packages.

```bash
# Example commands
git https://github.com/abin-m/local_event_platform.git
cd local_event_platform

virtualenv venv
source venv/bin/activate # Activating Virtual environment

pip install -r requirements.txt
```

#### Create an Account in Twilio and obtain the below details

    TWILIO_ACCOUNT_SID= your_account_sid
    TWILIO_AUTH_TOKEN= your_auth_token
    TWILIO_PHONE_NUMBER=your_twilio_phone_number

create a new .env file in root folder and add the above details

#### Run the celery

Befor that make sure that Reddis is running by entering the follwoing command.

    redis-cli ping
    # it will return PONG
    celery -A events_platform.celery worker -l info

Now we are ready to run our project

    cd events_platform
    python3 manage.py runserver # for Ubuntu or IOS
    python manage.py runserver # for Windows

# API documentation

Welcome to the Local Event Platform API documentation. This guide provides information on how to interact with the API endpoints to manage events.

### Registration/Sign UP

### Request

- **Method:** POST
- **URL:** `http://localhost:8000/api/register/`
- **Headers:** No specific headers are required.
- **Body:**

  ```
  {
  "username": "testuser",
  "email": "usertest@gmail.com",
  "password": "Test@12345",
  "phone_number":"+919188292137"
  }
  ```

### Response

    Status Code: 201 Created
    Response Body:
    {
    "refresh": "Your refresh token",
    "access": "your Access token"
    }

### Login/Sign In

### Request

- **Method:** POST
- **URL:** `http://localhost:8000/api/login/`
- **Headers:** No specific headers are required.
- **Body:**

  ```
  {
  "username": "your_username",
  "password": "your_password"
  }
  ```

### Response

    Status Code: 201 Created
    Response Body:
    {
    "refresh": "your_refresh_token",
    "access": "your_access_token"
    }

### Refresh Token

### Request

- **Method:** POST
- **URL:** `http://localhost:8000/api/refresh-token/`
- **Headers:** No specific headers are required.
- **Body:**

  ```
  {
  "refresh_token": "your_refresh_token"
  }
  ```

### Response

    Status Code: 201 Created
    Response Body:
    {
     "access": "your_new_access_token"
    }

### Event List

### Request

- **Method:** GET
- **URL:** `http://localhost:8000/api/events/`
- **Headers:** Authorization: Bearer your_access_token

### Response

    Status Code: 201 Created
    Response Body:
    [
    {
    "id": 1,
    "event_title": "Event Title 1",
    "event_date": "YYYY-MM-DD",
    "event_time": "HH:MM",
    "event_location": "Event Location 1",
    "description": "Event Description 1",
    "creator": "your_username"
    },
    {
    "id": 2,
    "event_title": "Event Title 2",
    "event_date": "YYYY-MM-DD",
    "event_time": "HH:MM",
    "event_location": "Event Location 2",
    "description": "Event Description 2",
    "creator": "your_username"
    }

// ... other events
]

### CreateEvent

### Request

- **Method:** POST
- **URL:** `http://localhost:8000/api/events/`
- **Headers:** Authorization: Bearer your_access_token
- **Body:**

  ```
  {
  "event_title": "New Event Title",
  "event_date": "YYYY-MM-DD",
  "event_time": "HH:MM:SS",
  "event_location": "New Event Location",
  "description": "New Event Description"
  }

  ```

### Response

    Status Code: 201 Created
    Response Body:
    {
    "id": 1,
    "event_title": "New Event Title",
    "event_date": "YYYY-MM-DD",
    "event_time": "HH:MM:SS",
    "event_location": "New Event Location",
    "description": "New Event Description",
    "creator": "your_username"
    }

### UpdateEvent

### Request

- **Method:** PUT
- **URL:** `http://localhost:8000/api/events/1/` (Replace 1 with the actual event ID)
- **Headers:** Authorization: Bearer your_access_token
- **Body:**

  ```
  {
  "event_title": "New Event Title",
  "event_date": "YYYY-MM-DD",
  "event_time": "HH:MM:SS",
  "event_location": "New Event Location",
  "description": "New Event Description"
  }

  ```

### Response

    Status Code: 200 OK
    Response Body:
    {
    "id": 1,
    "event_title": "New Event Title",
    "event_date": "YYYY-MM-DD",
    "event_time": "HH:MM:SS",
    "event_location": "New Event Location",
    "description": "New Event Description",
    "creator": "your_username"
    }

### CancelEvent

### Request

- **Method:** PUT
- **URL:** `http://localhost:8000/api/events/1/` (Replace 1 with the actual event ID)
- **Headers:** Authorization: Bearer your_access_token

### Response

    Status Code: 204 No Content
    Response Body:
    {
    message: Event Cancelled Successfully.
    }
