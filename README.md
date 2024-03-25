<h1 align="center">E-Mail Project In REST API using GMAIL API, Flask, SQLAlchemy, SQLite, Docker</h1>


<div>
<img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" />
<img src="https://img.shields.io/badge/SQLAlchemy-red?style=for-the-badge&logo=sqlalchemy&logoColor=white" />
<img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
<img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
<img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" />
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/Gmail-EA4335?style=for-the-badge&logo=gmail&logoColor=white" />
</div>

## Tree of Directory

```
.
├── app.py
├── blocklist.py
├── client_secret.json
├── db.py
├── docker-compose.yml
├── Dockerfile
├── Google.py
├── instance
│   └── data.db
├── migrations
├── models
│   ├── __init__.py
│   └── user.py
├── README.md
├── requirements.txt
├── resources
│   └── user.py
├── schemas.py
├── settings.py
├── tasks.py
├── templates
│   └── email
│       ├── action.html
│       └── action.original.html
└── token_gmail_v1.pickle
```

## Description

This project demonstrates a simple REST API for user registration with email verification using the Gmail API. The application is built with Flask, SQLAlchemy, SQLite, and Docker.

## Endpoints

- **POST** `/register`: Register a new user and send a welcome email.
- **GET** `/user`: Get a list of all users.
- **DELETE** `/deleteall`: Delete all users from the database.

## Prerequisites

- Docker
- Docker Compose

## Installation & Run

1. Clone the repository:

    ```bash
    https://github.com/shakil1819/E-Mail-Register---REST-API-Implementation.git
    ```

2. Navigate to the project directory:


3. Build and run the Docker containers:

    ```bash
    docker-compose up --build
    ```
    ![Screencast from 2024-03-25 09-42-51](https://github.com/shakil1819/E-Mail-Register---REST-API-Implementation/assets/58840439/6d37963b-0324-4d49-a409-4f31c043b541)
    

## Configuration

Create a `.env` file in the project root and add the following:

```
REDIS_URL=redis://redis:6379/0
```


## Usage

### Register a User

To register a user, make a POST request to `/register` with the following JSON payload:

```json
{
    "username": "john_doe",
    "email": "john.doe@example.com",
    "password": "password123"
}
```

### Get All Users

To get a list of all users, make a GET request to `/user`.

### Delete All Users

To delete all users from the database, make a DELETE request to `/deleteall`.
![Screencast from 2024-03-25 10-03-47](https://github.com/shakil1819/E-Mail-Register---REST-API-Implementation/assets/58840439/fe60d474-eccd-4b60-a110-21505bec2c7a)


## Gmail API Setup

1. Enable the Gmail API and download the `client_secret.json`.
2. Place the `client_secret.json` in the project root directory.

## Additional Notes

- The email templates can be found in the `templates/email` directory.
- The Gmail token is stored in `token_gmail_v1.pickle`.


