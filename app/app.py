import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from app.db import Base, engine, get_db, SessionLocal
from app.models.Task import Task
from app.models.User import User
from app.schema.TaskSchema import TaskSchema, TaskUpdateSchema

from app.schema.UserSchema import UserSchema
from app.utils.jwt import create_access_token, decode_access_token
from app.utils.hashing import hash_password, verify_password


MAX_TASKS_PER_USER = 30
DATA_EXPIRY_MINUTES = 10

def purge_expired_data():
    db = SessionLocal()
    try:
        cutoff_time = datetime.utcnow() - timedelta(minutes=DATA_EXPIRY_MINUTES)
        db.query(Task).filter(Task.created_at < cutoff_time).delete(synchronize_session=False)
        db.query(User).filter(User.created_at < cutoff_time).delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error purging expired sandbox data: {e}")
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async def cleanup_loop():
        while True:
            await asyncio.sleep(60)
            purge_expired_data()
            
    cleanup_task = asyncio.create_task(cleanup_loop())
    yield
    cleanup_task.cancel()

app = FastAPI(
    title="Task Manager API",
    description=(
        "A backend application built using FastAPI to learn FastAPI and create a simple backend for task management.\n\n"
        "**Test Credentials**:\n"
        "- **Username**: `test_user`\n"
        "- **Password**: `1234`\n\n"
        "**Auto-Cleanup**: All sandbox accounts and tasks automatically self-destruct after **10 minutes** to keep storage clean."
    ),
    version="1.0.0",
    lifespan=lifespan
)


Base.metadata.create_all(bind=engine)

def get_current_user(token: str = Header(None), db: Session = Depends(get_db)) -> User:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token.")

    username = payload.get("sub")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")
    return user

@app.post("/login")
def login(user: UserSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password.")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": db_user.username}, expires_delta=access_token_expires)

    return {"message": "Login Successfull", "access_token": access_token}

@app.post("/signin")
def sign_in(user: UserSchema, db: Session = Depends(get_db)):
    hashed_pwd = hash_password(user.password)
    new_user = User(
        username = user.username,
        password = hashed_pwd
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "New User created successfully...!"}

@app.get("/tasks")
def get_tasks(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Task).filter(Task.user_id == user.id).all()

@app.get("/tasks/{task_id}")
def get_single_task(task_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.user_id == user.id, Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")
    return {"task": task}

@app.post("/tasks")
def add_task(task: TaskSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task_count = db.query(Task).filter(Task.user_id == user.id).count()
    if task_count >= MAX_TASKS_PER_USER:
        raise HTTPException(
            status_code=400, 
            detail=f"Task limit reached! Maximum allowed is {MAX_TASKS_PER_USER} tasks per user."
        )
    new_task = Task(
        title = task.title,
        description = task.description,
        completed = task.completed,
        user_id = user.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message": "Task added successfully...!", "id": new_task.id}

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated: TaskUpdateSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.user_id == user.id, Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")
    
    update_data = updated.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return {"message": "Task updated successfully...!", "task": task}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.user_id == user.id, Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully...!"}

@app.delete("/tasks")
def delete_all_tasks(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.query(Task).filter(Task.user_id == user.id).delete()
    db.commit()
    return {"message": "Deleted all tasks."}