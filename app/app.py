from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from datetime import timedelta

from db import Base, engine, get_db
from models.Task import Task
from models.User import User
from schema.TaskSchema import TaskSchema
from schema.UserSchema import UserSchema
from utils.jwt import create_access_token, decode_access_token
from utils.hashing import hash_password, verify_password

app = FastAPI(title="Task Manager API")
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
def update_task(task_id: int, updated: TaskSchema, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.user_id == user.id, Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")
    
    task.title = updated.title
    task.description = updated.description
    task.completed = updated.completed
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