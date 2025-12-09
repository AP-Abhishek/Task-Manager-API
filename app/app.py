from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from db import Base, engine, get_db
from models.Task import Task
from models.User import User
from schema.TaskSchema import TaskSchema
from schema.UserSchema import UserSchema

app = FastAPI(title="Task Manager API")
Base.metadata.create_all(bind=engine)

def get_current_user(token: str, db: Session):
    if not token.startswith("token_"):
        return None
    user_id = token.replace("token_", "")
    user = db.query(User).filter(User.id == user_id).first()
    return user

@app.post("/login")
def login(user: UserSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=400, detail="Invalid username or password.")

    session_token = f"token_{db_user.id}"
    return {"message": "Login Successfull", "session": session_token}

@app.post("/signin")
def sign_in(user: UserSchema, db: Session = Depends(get_db)):
    new_user = User(
        username = user.username,
        password = user.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "New User created successfully...!"}

@app.get("/tasks")
def get_tasks(token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid session.")
    return db.query(Task).filter(Task.user_id == user.id).all()

@app.get("/tasks/{task_id}")
def get_single_task(task_id: int, token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid session.")
    
    task = db.query(Task).filter(Task.user_id == user.id, Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")
    return {"task": task}

@app.post("/tasks")
def add_task(task: TaskSchema, token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid session.")
    
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
def update_task(task_id: int, token: str, updated: TaskSchema, db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid session.")

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
def delete_task(task_id: int, token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid session.")
    
    task = db.query(Task).filter(Task.user_id == user.id, Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully...!"}

@app.delete("/tasks")
def delete_all_tasks(token: str, db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid session.")
    
    db.query(Task).filter(Task.user_id == user.id).delete()
    db.commit()
    return {"message": "Deleted all tasks."}