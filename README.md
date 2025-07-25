#  FastAPI Social Media App

A simple and scalable **RESTful API** built with **FastAPI** for a social media platform. This project includes user authentication using **JWT**, post creation, and CRUD operations. Designed for learning, showcasing skills, and building real-world experience.

---

## Features

-  User Registration & Login
-  JWT-based Authentication
-  Create, Read, Update, Delete (CRUD) for Posts
-  View All Posts or User-Specific Posts
-  Follow other users (Optional: Advanced feature)
-  SQLite or PostgreSQL DB support

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| [FastAPI](https://fastapi.tiangolo.com/) | Web framework |
| [Uvicorn](https://www.uvicorn.org/) | ASGI server |
| [JWT (PyJWT)](https://pyjwt.readthedocs.io/en/latest/) | Auth tokens |
| [Pydantic](https://docs.pydantic.dev/) | Data validation |
| [SQLAlchemy](https://www.sqlalchemy.org/) | ORM (if used) |
| [SQLite/PostgreSQL](https://www.sqlite.org/) | Database |
| [Python 3.10+](https://www.python.org/) | Language |

---

## Project Structure

fastapi_social_media_/
├── app/
│ ├── main.py # Entry point
│ ├── models.py # SQLAlchemy models
│ ├── schemas.py # Pydantic models
│ ├── routes/
│ │ ├── auth.py # Login/Register routes
│ │ └── posts.py # CRUD post routes
│ ├── database.py # DB connection
│ └── utils.py # Helper functions (e.g., password hashing)
├── requirements.txt # Dependencies
├── README.md # Project info
└── .env # Secret keys, DB URL


