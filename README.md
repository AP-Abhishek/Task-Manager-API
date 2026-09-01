# Task Manager API

Task Manager API is a robust, RESTful backend web service engineered to securely handle user authentication and streamline comprehensive task management workflows.

Operating as a fully modular backend architecture, the application provides secure, authenticated access to task creation, tracking, and modification. It prioritizes data integrity and security by utilizing JSON Web Tokens (JWT) for session management and strict Pydantic schemas to validate data across all incoming API requests.

---

## Key Highlights of the Project

- **Modern Backend Stack:** Built natively with Python and FastAPI, leveraging SQLAlchemy for ORM-based database interactions and PostgreSQL for relational data storage.
- **Secure Authentication & Validation:** Implements secure JWT-based authentication and bcrypt password hashing, paired with strict input validation and support for dynamic partial data updates (`exclude_unset=True`).
- **Automated Background Processes:** Engineered with a custom background lifespan worker designed to automatically detect and purge temporary sandbox accounts and stale tasks after 10 minutes, ensuring continuous database optimization.
- **Interactive API Documentation:** Automatically generates and serves interactive OpenAPI documentation via Swagger UI (`/docs`) and ReDoc (`/redoc`), enabling seamless developer onboarding and immediate endpoint testing.

---


## API Endpoints Summary

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| **POST** | `/signin` | Register a new user account | No |
| **POST** | `/login` | Authenticate user and receive JWT access token | No |
| **GET** | `/tasks` | Retrieve all tasks belonging to current user | Yes |
| **GET** | `/tasks/{task_id}` | Retrieve specific task details by ID | Yes |
| **POST** | `/tasks` | Create a new task (Max 30 tasks per user) | Yes |
| **PUT** | `/tasks/{task_id}` | Update existing task attributes partially or fully | Yes |
| **DELETE** | `/tasks/{task_id}` | Delete a specific task by ID | Yes |
| **DELETE** | `/tasks` | Delete all tasks for the logged-in user | Yes |

---

## Local Testing & Interactive Documentation

Once the application server is running locally, you can access the interactive Swagger UI documentation at:

* **Swagger UI:** `http://127.0.0.1:8000/docs`
* **ReDoc:** `http://127.0.0.1:8000/redoc`

### How to Test Endpoints:
1. Open `http://127.0.0.1:8000/docs` in your browser.
2. Use the **`POST /signin`** endpoint to register a new user account with your choice of username and password.
3. Use the **`POST /login`** endpoint to authenticate. Copy the returned `access_token`.
4. Click the **Authorize** button (top right of Swagger UI) or pass the token in the `token` header to access protected task management endpoints (`/tasks`).

---

## Environment Setup & Running the Application

To run the application locally on your machine:

### Prerequisites
* Python 3.8 or higher installed on your system.
* PostgreSQL database instance running locally or hosted.
* Git installed.

### Step 1: Clone the Repository
```bash
git clone https://github.com/AP-Abhishek/Task-Manager-API.git
cd Task-Manager-API
```

### Step 2: Create & Activate Virtual Environment
* **On Windows (Command Prompt / PowerShell):**
  ```powershell
  python -m venv fastapi
  .\fastapi\Scripts\Activate.ps1
  ```
* **On macOS / Linux:**
  ```bash
  python3 -m venv fastapi
  source fastapi/bin/activate
  ```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the root directory with the following variables:
```env
DATABASE_URL=your_database_url                 # PostgreSQL connection string (e.g., postgresql://user:password@localhost:5432/dbname)
SECRET_KEY=your_secret_key                     # Secret key for JWT signing
ALGORITHM=HS256                                # Token encoding algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=30                 # Token expiration duration in minutes
```


### Step 5: Launch the Server
```bash
python main.py
```
Or run directly with Uvicorn:
```bash
uvicorn main:app --reload
```

Once running, access the interactive Swagger UI at: `http://127.0.0.1:8000/docs`

---

## Project Structure

```text
Task-Manager-API/
├── app/
│   ├── models/            # SQLAlchemy database models (User.py, Task.py)
│   ├── schema/            # Pydantic validation schemas (UserSchema.py, TaskSchema.py)
│   ├── utils/             # Helper utilities (hashing.py, jwt.py)
│   ├── __init__.py        # Package initialization marker
│   ├── app.py             # FastAPI routes, lifespan worker & middleware
│   └── db.py              # Database engine & session configuration
├── .env                   # Environment variable settings
├── .gitignore             # Git ignore configuration
├── main.py                # Single application entry point
├── README.md              # Project documentation
└── requirements.txt       # Application dependencies
```