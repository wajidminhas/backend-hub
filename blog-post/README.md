

# FastAPI Blog API

A REST API for managing blog posts and users, built with FastAPI, SQLModel, and SQLite. Organized with separate models, CRUD operations, and routes.

## Project Structure
```
fastapi-blog/
├── app/
│   ├── main.py         # FastAPI app
│   ├── database.py     # SQLite connection
│   ├── models/         # SQLModel schemas
│   │   ├── post.py
│   │   ├── user.py
│   │   ├── comment.py
│   ├── routes/         # API endpoints
│   │   ├── post.py
│   │   ├── user.py
│   │   ├── comment.py
│   ├── crud/           # Database operations
│   │   ├── post.py
│   │   ├── user.py
│   │   ├── comment.py
├── pyproject.toml      # Poetry dependencies
├── README.md
```

## Setup
1. **Navigate to Project**:
   ```bash
   cd fastapi-blog
   ```

2. **Install Poetry** (if not installed):
   ```bash
   pip install poetry
   ```

3. **Add Dependencies**:
   ```bash
   poetry add fastapi sqlmodel uvicorn
   ```

4. **Activate Environment**:
   ```bash
   poetry shell
   ```

5. **Install Dependencies**:
   ```bash
   poetry install
   ```

## Running the App
```bash
poetry run uvicorn app.main:app --reload
```
- Access at `http://127.0.0.1:8000`.

## Usage
- **API Docs**: Open `http://127.0.0.1:8000/docs` for Swagger UI.
- **Endpoints**:
  - `POST /users/`: Create a user.
    ```json
    {"username": "johndoe", "email": "john@example.com"}
    ```
  - `GET /users/`: List all users.
  - `POST /posts/`: Create a post.
    ```json
    {"title": "My Post", "content": "Hello!", "author_id": 1}
    ```
  - `GET /posts/`: List all posts.

## Database
- SQLite (`blog.db`) stores `post`, `user`, and `comment` tables.