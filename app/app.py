from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from db import Base, engine, get_db
from models.Task import Task
from models.User import User
from schema.TaskSchema import TaskSchema
from schema.UserSchema import UserSchema

app = FastAPI(title="Task Manager API")
Base.metadata.create_all(bind=engine)

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
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

@app.get("/tasks/{task_id}")
def get_single_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")
    return {"task": task}

@app.post("/tasks")
def add_task(task: TaskSchema, db: Session = Depends(get_db)):
    new_task = Task(
        title = task.title,
        description = task.description,
        completed = task.completed
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message": "Task added successfully...!", "id": new_task.id}

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated: TaskSchema, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")
    task.title = updated.title
    task.description = updated.description
    task.completed = updated.completed
    db.commit()
    db.refresh(task)
    return {"message": "Task updated successfully...!", "task": task}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully...!"}

@app.delete("/tasks")
def delete_all_tasks(db: Session = Depends(get_db)):
    db.query(Task).delete()
    db.commit()
    return {"message": "Deleted all tasks."}