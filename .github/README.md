# Pre3

Pre3 is a `course management system` that will help a academic institution to manage their courses, students, and faculty. It will also help students to plan their courses and track their progress.

## Features

Pre3 is playing with a role of user, No matter if you are a `student`, `instructor`, or `admin`. Pre3 will help you to manage your courses, students, and faculty.

### ROLE

Role is a key feature of Pre3. Each user will have a role. Role will help Pre3 to understand the user and provide the features accordingly.

> ***NOTE*** Each role holds a set of permissions. Permissions are the key to access the features. and each role will not have rights to access the features which are not allowed by the permissions.

- GUEST: A user who is not logged in.
- ADMIN: A special user who can manage the whole system.
- STUDENT: A user who is a student. They can manage their courses and track their learning progress and plan their courses with visual representation of the course tree.
- Lecturer: A user who is an lecturer. They can manage their courses and students. They can also track the progress of their students.

### Prerequisite Tree

Pre3 will provide a visual representation of the course tree. It will help students to plan their courses and track their progress.

> **NOTE** `THIS FEATURE IS CURRENTLY UNDER DEVELOPMENT`

### Course Management

Pre3 will provide a feature to manage the courses. Admin can manage the courses and students. They can also track the progress of their students.

> **NOTE** `THIS FEATURE IS CURRENTLY UNDER DEVELOPMENT`

## Technologies

### Frontend

1. Bootstrap 5 as a CSS framework
2. JavaScript

### Backend

1. Flask as a web framework
2. DJango as a backend framework
3. Jinja2 as a templating engine
3. Gunicorn as a WSGI server
4. PostgresSQL as a database
5. SQLAlchemy as an ORM
6. Flask-Login for user authentication
7. Flask-WTF for form handling and validation
8. SheetJS for handling the excel files and converting them into JSON

### Deployment

1. Docker for containerization

### SERVICES

1. Google Sheets API for handling the course data
2. Google SSO for user authentication

## Installation

### Prerequisites

- Python 3.8 or higher
- Docker
- Google Sheets API Key
- Google SSO Key
- PostgresSQL
- Make

### Steps

1. Clone the repository

```bash
git clone git@github.com:AppleBoiy/pre3.git
```

2. build the docker image using `Makefile`

```bash
make build
```

This will build the docker image and create a container for the application.

    localhost:56733 -> 80 is the port for the application
    localhost:5432 -> 5432 is the port for the database

3. Seed the database

```bash
make seed-d
```

This will seed the database with the initial data.

## Usage

### Development

The application is running on the `localhost:56733` and the database is running on the `localhost:5432`.

#### Set of commands

There are a set of commands that you can use to manage the application.

- `make build` -> Build the docker image
    - `make create-db` -> Create the database
    - `make seed-db` -> Seed the database
    - `make drop-db` -> Drop the database
- `make remote-dk` -> remote to the remote docker container
- `make remote-db` -> remote to the remote database

and many more. you can check the `Makefile` for more commands.

### References

We have use a lot of references to build this application. You can check the references in the `../docs/REFERENCES.md` file.

---

Get help: [Post in our discussion board](https://github.com/AppleBoiy/pre3/discussions) &bull; [Review the GitHub status page](https://www.githubstatus.com/)

&copy; 2023 AppleBoiy &bull; [Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md) &bull; [MIT License](../LICENSE)