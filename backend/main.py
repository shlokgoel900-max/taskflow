import time
from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import User, Project, Task
from .schemas import UserCreate, UserOut, ProjectCreate, ProjectOut, TaskCreate, TaskOut, TaskUpdate, QuickAdd
from .algorithms import insertion_sort, binary_search, linear_search
from .quick_add import mock_parse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

@app.middleware("http")
async def request_logger(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = (time.perf_counter() - start) * 1000
    print(f"{request.method} {request.url.path} {elapsed:.2f}ms")
    return response

@app.post("/users", response_model=UserOut, status_code=201)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(422, "email already exists")
    user = User(**data.model_dump())
    db.add(user); db.commit(); db.refresh(user)
    return user

@app.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.post("/projects", response_model=ProjectOut, status_code=201)
def create_project(data: ProjectCreate, db: Session = Depends(get_db)):
    if not db.get(User, data.owner_id):
        raise HTTPException(422, "owner_id does not reference an existing user")
    project = Project(**data.model_dump())
    db.add(project); db.commit(); db.refresh(project)
    return project

@app.get("/projects", response_model=list[ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()

def task_to_dict(t):
    return {"id": t.id, "title": t.title, "priority": t.priority,
            "due_date": t.due_date, "status": t.status, "project_id": t.project_id}

@app.post("/tasks", response_model=TaskOut, status_code=201)
def create_task(data: TaskCreate, db: Session = Depends(get_db)):
    if not db.get(Project, data.project_id):
        raise HTTPException(422, "project_id does not reference an existing project")
    task = Task(**data.model_dump())
    db.add(task); db.commit(); db.refresh(task)
    return task

@app.get("/tasks", response_model=list[TaskOut])
def list_tasks(sort: str | None = Query(default=None), db: Session = Depends(get_db)):
    tasks = [task_to_dict(t) for t in db.query(Task).all()]
    if sort == "priority":
        rank = {"low": 1, "medium": 2, "high": 3}
        for t in tasks:
            t["_priority_rank"] = rank[t["priority"]]
        insertion_sort(tasks, "_priority_rank")
        for t in tasks:
            t.pop("_priority_rank", None)
    elif sort == "due_date":
        insertion_sort(tasks, "due_date")
    return tasks

@app.get("/tasks/search", response_model=TaskOut)
def search_tasks(title: str, algo: str = "binary", db: Session = Depends(get_db)):
    index = [{"id": t.id, "title": t.title} for t in db.query(Task).all()]
    if algo == "binary":
        insertion_sort(index, "title")
        pos = binary_search(index, title, "title")
    elif algo == "linear":
        pos = linear_search(index, title, "title")
    else:
        raise HTTPException(422, "algo must be binary or linear")
    if pos == -1:
        raise HTTPException(404, "task not found")
    return db.get(Task, index[pos]["id"])

@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task: raise HTTPException(404, "task not found")
    return task

@app.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task: raise HTTPException(404, "task not found")
    values = data.model_dump(exclude_unset=True)
    if "project_id" in values and not db.get(Project, values["project_id"]):
        raise HTTPException(422, "project_id does not reference an existing project")
    for k, v in values.items(): setattr(task, k, v)
    db.commit(); db.refresh(task)
    return task

@app.delete("/tasks/{task_id}", status_code=200)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task: raise HTTPException(404, "task not found")
    db.delete(task); db.commit()
    return {"message": "task deleted", "id": task_id}

@app.get("/projects/statistics")
def project_statistics(db: Session = Depends(get_db)):
    rows = (
        db.query(Project.id, Project.name, func.count(Task.id).label("task_count"))
        .outerjoin(Task, Task.project_id == Project.id)
        .group_by(Project.id, Project.name)
        .all()
    )
    return [{"project_id": r.id, "project_name": r.name, "task_count": r.task_count}
            for r in rows]

@app.post("/tasks/quick-add", response_model=TaskOut, status_code=201)
def quick_add(data: QuickAdd, db: Session = Depends(get_db)):
    if not db.get(Project, data.project_id):
        raise HTTPException(422, "project_id does not reference an existing project")
    parsed = mock_parse(data.description)
    task_data = TaskCreate(
        title=parsed["title"],
        priority=parsed["priority"],
        due_date=parsed["due_date_hint"],
        project_id=data.project_id,
        status="todo",
    )
    task = Task(**task_data.model_dump())
    db.add(task); db.commit(); db.refresh(task)
    return task
