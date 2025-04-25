URL Shortener

A simple and efficient URL shortening service built with FastAPI and SQLModel. This application allows users to shorten long URLs into compact, shareable links and tracks the number of clicks on each shortened URL. The backend uses SQLModel for database operations with SQLite (configurable for other databases like PostgreSQL) and FastAPI for a high-performance API.

Features





Shorten URLs with a 6-character unique short code.



Redirect users to the original URL using the short code.



Track the number of clicks for each shortened URL.



Validate URLs to ensure they are valid HTTP/HTTPS links.



Store URL data with timestamps and unique identifiers.



API documentation via Swagger UI.

Tech Stack





FastAPI: High-performance web framework for building APIs.



SQLModel: ORM combining SQLAlchemy and Pydantic for database operations and validation.



SQLite: Lightweight database (configurable for PostgreSQL, MySQL, etc.).



Python: Backend programming language (3.8+ recommended).

Prerequisites





Python 3.8 or higher



pip (Python package manager)



Virtualenv (optional but recommended)

Installation





Clone the Repository:

git clone https://github.com/your-username/url-shortener```bash
cd url-shortener



Create a Virtual Environment (optional but recommended):

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate



Install Dependencies:

pip install fastapi sqlmodel uvicorn pydantic



Set Up the Database:





The project uses SQLite by default (urls.db). No additional setup is required.



To use another database (e.g., PostgreSQL), update the DATABASE_URL in models.py (e.g., postgresql://user:password@localhost/dbname).

Running the Application





Start the FastAPI Server:

uvicorn main:app --reload





--reload enables auto-reload for development.



The server will run at http://localhost:8000.



Access the API:





Open http://localhost:8000/docs in your browser for the interactive Swagger UI.



Use the /shorten endpoint to create a shortened URL.



Use the /{short_code} endpoint to redirect to the original URL.

API Endpoints

POST /shorten





Description: Create a shortened URL.



Request Body:

{
  "original_url": "https://example.com"
}



Response:

{
  "id": "uuid-string",
  "original_url": "https://example.com",
  "short_code": "abc123",
  "created_at": "2025-04-25T12:00:00Z",
  "clicks": 0
}

GET /{short_code}





Description: Redirect to the original URL and increment the click count.



Response: JSON with the original URL or a 404 error if the short code is invalid.

{
  "original_url": "https://example.com"
}

Configuration





Database: Modify DATABASE_URL in models.py to use a different database.



Short Code Length: Adjust max_length in the URL model and the generation logic in main.py.



Production: Set echo=False in create_engine and avoid --reload in uvicorn.

Example Usage





Shorten a URL:

curl -X POST http://localhost:8000/shorten -H "Content-Type: application/json" -d '{"original_url": "https://example.com"}'

Output:

{
  "id": "7b9f2e3a-8f1c-4e9d-b7a2-f8e6c1b4d2a5",
  "original_url": "https://example.com",
  "short_code": "abc123",
  "created_at": "2025-04-25T12:00:00Z",
  "clicks": 0
}



Access the shortened URL:

curl http://localhost:8000/abc123

Output:

{
  "original_url": "https://example.com"
}

Troubleshooting





Database Errors: Ensure the database is running and the DATABASE_URL is correct.



Port Conflicts: Change the port with uvicorn main:app --port 8001.



Validation Errors: Ensure the original_url is a valid HTTP/HTTPS URL.

Contributing

Feel free to submit issues or pull requests to improve the project. Follow standard GitHub workflows for contributions.

License

MIT License. See LICENSE for details.