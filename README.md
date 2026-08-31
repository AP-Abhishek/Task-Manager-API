# Task Manager API

A RESTful backend web service built using Python, FastAPI, SQLAlchemy, and PostgreSQL to manage user authentication and task management workflows.

---

## Project Overview & Workflow

The core API architecture and endpoints are implemented in modular FastAPI components. The application follows a complete end-to-end backend engineering workflow:

1. **User Authentication:** Handles user registration (`/signin`) and authentication (`/login`), generating JSON Web Tokens (JWT) and securing passwords via bcrypt hashing.
2. **Task CRUD Operations:** Provides endpoints to create, read, update, and delete tasks associated with authenticated users.
3. **Partial Field Updates:** Supports partial task updates (`PUT /tasks/{id}`) using Pydantic schemas and `exclude_unset=True`.
4. **Input Validation:** Enforces strict data validation on usernames, passwords, titles, and descriptions using Pydantic `Field` constraints.
5. **Sandbox Auto-Cleanup:** Features a background lifespan worker that automatically purges sandbox accounts and tasks created more than 10 minutes ago.
6. **Interactive Documentation:** Serves automatic OpenAPI documentation via Swagger UI (`/docs`) and ReDoc (`/redoc`).

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

## Test Credentials

For quick testing via Swagger UI (`/docs`) or Postman, you can use the pre-configured sandbox credentials:

* **Username:** `test_user`
* **Password:** `1234`

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