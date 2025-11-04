# My Micro SaaS

A FastAPI-based micro SaaS application with user authentication and post management.

## Features

- **User Management**: Register users with email and secure password hashing (bcrypt_sha256)
- **JWT Authentication**: Token-based authentication using OAuth2 with Bearer tokens
- **Post Management**: Create, read, and update posts with ownership enforcement
- **PostgreSQL Database**: SQLAlchemy ORM with PostgreSQL backend
- **API Documentation**: Auto-generated interactive docs via FastAPI

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Relational database
- **Passlib + Bcrypt**: Password hashing with bcrypt_sha256
- **Python-Jose**: JWT token handling
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server

## Project Structure

```
my_micro_saas/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app and route definitions
│   ├── models.py        # SQLAlchemy database models
│   ├── schemas.py       # Pydantic schemas for validation
│   ├── crud.py          # Database operations
│   ├── security.py      # Authentication and password hashing
│   ├── hashing.py       # Password utility functions
│   └── database.py      # Database configuration
├── agents/              # AI agent modules
├── requirements.txt     # Python dependencies
├── docker-compose.yml   # Docker services configuration
├── Dockerfile           # Container image definition
└── .env                 # Environment variables (not in git)
```

## Prerequisites

- Python 3.9+
- PostgreSQL
- pip and virtualenv

## Setup

### 1. Clone the repository

```bash
git clone <url>
cd my_micro_saas
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key-here
```

Generate a secret key:

```bash
openssl rand -hex 32
```

### 5. Set up the database

Make sure PostgreSQL is running, then the tables will be created automatically on first run.

Alternatively, use Docker Compose:

```bash
docker-compose up -d
```

### 6. Run the application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## API Endpoints

### Authentication

- **POST** `/token` - Get access token (login)
  - Form data: `username` (email), `password`
  - Returns: `access_token`, `token_type`

### Users

- **POST** `/users` - Register a new user
  - Body: `{"email": "user@example.com", "password": "yourpassword"}`
  - Returns: User object

### Posts

- **POST** `/posts` - Create a new post (requires authentication)

  - Headers: `Authorization: Bearer <token>`
  - Body: `{"title": "Post Title", "content": "Post content"}`
  - Returns: Post object

- **GET** `/posts` - List all posts (requires authentication)

  - Headers: `Authorization: Bearer <token>`
  - Query params: `skip` (default: 0), `limit` (default: 10)
  - Returns: List of posts

- **PATCH** `/posts/{post_id}` - Update a post (requires authentication & ownership)
  - Headers: `Authorization: Bearer <token>`
  - Body: `{"title": "New Title"}` (partial updates supported)
  - Returns: Updated post object

## Interactive API Documentation

Visit `http://127.0.0.1:8000/docs` for Swagger UI documentation.

Visit `http://127.0.0.1:8000/redoc` for ReDoc documentation.

## Development

### Running tests

```bash
pytest
```

### Code formatting

```bash
black .
```

### Linting

```bash
flake8 .
```

## Docker Deployment

Build and run with Docker Compose:

```bash
docker-compose up --build
```

## Security Notes

- Passwords are hashed using `bcrypt_sha256` to avoid the 72-byte bcrypt limitation
- JWT tokens expire after 30 minutes (configurable in `security.py`)
- Always use HTTPS in production
- Keep your `SECRET_KEY` secure and never commit `.env` to version control

## License

See [LICENSE](LICENSE) file for details.
