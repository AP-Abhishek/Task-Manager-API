from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from db import Base, engine, get_db
from models.Task import Task
from schema.TaskSchema import TaskSchema

app = FastAPI(title="Task Manager API")
Base.metadata.create_all(bind=engine)

@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

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
