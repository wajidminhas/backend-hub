# User Services API

A FastAPI-based user authentication service with JWT-based OAuth2 authentication, SQLModel for database operations, and PostgreSQL as the database. This project supports user registration, login, and profile retrieval, using secure password hashing with `bcrypt`.

## Project Structure

```
user_services/
├── app/
│   ├── main.py              # FastAPI app initialization
│   ├── router/
│   │   ├── user.py          # User authentication and profile endpoints
│   ├── models/
│   │   ├── user.py          # SQLModel Users model
├── .env                     # Environment variables (SECRET_KEY)
├── pyproject.toml           # Poetry dependencies
├── README.md                # Project documentation
```

## Features

- **User Authentication**: Register and login users with OAuth2 password flow.
- **JWT Tokens**: Secure JWT-based authentication with configurable expiry.
- **Password Hashing**: Secure password storage using `bcrypt`.
- **Database**: PostgreSQL with SQLModel for ORM.
- **Dependency Management**: Poetry for reproducible environments.

## Prerequisites

- Python 3.10+
- PostgreSQL database
- Poetry for dependency management
- Git (optional, for cloning)

## Installation

1. **Clone the Repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd user_services
   ```

2. **Install Dependencies**:
   Use Poetry to set up the virtual environment and install dependencies:
   ```bash
   poetry install
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=932a9a8a39cba70f83e0f0b095b6892a31b5923e28383fa6920c20ec970419cb
   DATABASE_URL=postgresql+psycopg://user:password@localhost/dbname
   ```
   - Replace `user`, `password`, and `dbname` with your PostgreSQL credentials.
   - Ensure `.env` is added to `.gitignore`.

4. **Set Up PostgreSQL Database**:
   - Create a PostgreSQL database:
     ```bash
     psql -U postgres -c "CREATE DATABASE dbname;"
     ```
   - Initialize the database schema (run once):
     ```python
     from sqlmodel import SQLModel, create_engine
     from app.models.user import Users

     DATABASE_URL = "postgresql+psycopg://user:password@localhost/dbname"
     engine = create_engine(DATABASE_URL)
     SQLModel.metadata.create_all(engine)
     ```

5. **Run the Application**:
   Start the FastAPI server with Uvicorn:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

### Authentication
- **POST /user/token**
  - **Description**: Authenticate a user and return a JWT access token.
  - **Request**:
    ```bash
    curl -X POST http://127.0.0.1:8000/user/token \
         -H "Content-Type: application/x-www-form-urlencoded" \
         -d "username=testuser&password=testpass"
    ```
  - **Response**:
    ```json
    {
      "access_token": "<jwt-token>",
      "token_type": "bearer"
    }
    ```
  - **Errors**:
    - `401 Unauthorized`: Invalid username or password.

- **GET /user/user**
  - **Description**: Retrieve the authenticated user’s profile.
  - **Request**:
    ```bash
    curl -X GET http://127.0.0.1:8000/user/user \
         -H "Authorization: Bearer <jwt-token>"
    ```
  - **Response**:
    ```json
    {
      "username": "testuser",
      "email": "test@example.com",
      "id": 1
    }
    ```
  - **Errors**:
    - `401 Unauthorized`: Invalid or expired token.
    - `404 Not Found`: User not found.

## Usage

1. **Register a User**:
   - Ensure your application has a registration endpoint or manually insert a user into the database with a hashed password:
     ```python
     from app.router.user import hashed_password
     from sqlmodel import Session
     from app.models.user import Users

     with Session(engine) as session:
         user = Users(
             username="testuser",
             email="test@example.com",
             hash_password=hashed_password("testpass")
         )
         session.add(user)
         session.commit()
     ```

2. **Authenticate**:
   - Send a `POST /user/token` request with `username` and `password` to obtain a JWT.

3. **Access Protected Routes**:
   - Use the JWT in the `Authorization: Bearer <jwt-token>` header to access `/user/user`.

4. **View API Docs**:
   - Open `http://127.0.0.1:8000/docs` for interactive Swagger UI.

## Dependencies

Defined in `pyproject.toml`:
- `fastapi`: ^0.115.12
- `sqlmodel`: ^0.0.24
- `uvicorn`: ^0.34.2
- `psycopg`: ^3.2.7
- `python-jose[cryptography]`: ^3.4.0
- `passlib[bcrypt]`: ^1.7.4
- `bcrypt`: 4.0.1
- `python-multipart`: ^0.0.20
- `python-dotenv`: ^1.0.0

To update dependencies:
```bash
poetry lock --no-update
poetry install
```

## Troubleshooting

- **404 Not Found for /user/token**:
  - Ensure `app.include_router(user_router)` is in `app/main.py`.
  - Verify the request URL is `/user/token` (due to `prefix="/user"`).
  - Check registered routes:
    ```bash
    poetry run python -c "from app.main import app; print([route.path for route in app.routes])"
    ```

- **401 Unauthorized**:
  - Verify the username and password exist in the database.
  - Ensure the JWT is valid and not expired (`EXPIRY_TIME=30` minutes).

- **bcrypt Errors**:
  - Confirm `bcrypt==4.0.1` is installed:
    ```bash
    poetry run pip show bcrypt
    ```
  - Clear Poetry cache and reinstall if issues persist:
    ```bash
    poetry cache clear --all pypi
    rm -rf ~/.cache/pypoetry/virtualenvs/user-services-izxZFvRX-py3.10
    poetry install
    ```

- **Database Issues**:
  - Ensure `DATABASE_URL` in `.env` is correct.
  - Verify PostgreSQL is running and the database exists.

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/xyz`).
3. Commit changes (`git commit -m "Add feature xyz"`).
4. Push to the branch (`git push origin feature/xyz`).
5. Open a pull request.

