from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import engine, get_db
import models
import datetime

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskMaster")

templates = Jinja2Templates(directory="templates")


# -------- Pydantic Schema --------

class TaskUpdate(BaseModel):
    title: str
    description: str
    priority: str


# -------- API ROUTES --------

@app.get("/api/tasks")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()


@app.post("/api/tasks")
def create_task(title: str, description: str = "", priority: str = "medium", db: Session = Depends(get_db)):

    task = models.Task(
        title=title,
        description=description,
        priority=priority
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


@app.patch("/api/tasks/{task_id}/complete")
def complete_task(task_id: int, db: Session = Depends(get_db)):

    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = True
    db.commit()

    return {"status": "updated"}


@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):

    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"status": "deleted"}


# -------- EDIT TASK (FIXED) --------

@app.put("/api/tasks/{task_id}")
def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db)):

    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = task_data.title
    task.description = task_data.description
    task.priority = task_data.priority

    db.commit()
    db.refresh(task)

    return task


# -------- HTML ROUTES --------

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(get_db)):

    tasks = db.query(models.Task).all()

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "tasks": tasks}
    )


@app.post("/add-task")
def add_task_form(
    title: str = Form(...),
    description: str = Form(""),
    priority: str = Form("medium"),
    due_date: str = Form(""),
    db: Session = Depends(get_db)
):

    parsed_date = None

    if due_date:
        parsed_date = datetime.datetime.strptime(due_date, "%Y-%m-%d")

    task = models.Task(
        title=title,
        description=description,
        priority=priority,
        due_date=parsed_date
    )

    db.add(task)
    db.commit()

    return RedirectResponse(url="/", status_code=303)