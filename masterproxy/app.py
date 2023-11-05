from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
from colorama import init as colorama_init
from db import schemas

import db

colorama_init(autoreset=True)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/register", response_model=schemas.ResponseOK | schemas.ResponseError)
async def registration(user_info: schemas.User):
    session = db.Session()
    existing_user = session.query(db.models.User).filter_by(email=user_info.email).first()
    if existing_user:
        session.close()
        return schemas.ResponseError(error_code=409, description="User with this email already exists")
    if len(user_info.password) < 8:
        session.close()
        return schemas.ResponseError(error_code=400, description="Password is too weak")
    new_user = db.models.User(email=user_info.email, password=user_info.password)
    session.add(new_user)
    session.commit()
    session.close()
    return schemas.ResponseOK(result=user_info.dict())


@app.post("/signin", response_model=schemas.ResponseOK | schemas.ResponseError)
async def signin(user_info: schemas.User):
    session = db.Session()
    user = session.query(db.models.User).filter_by(email=user_info.email).first()
    if not user or user.password != user_info.password:
        session.close()
        return schemas.ResponseError(error_code=401, description="Invalid email or password")
    session.close()
    return schemas.ResponseOK(result={"authenticated": True})


@app.post("/createTask", response_model=schemas.ResponseOK | schemas.ResponseError)
async def compute(create_task_info: schemas.CreateTask):
    session = db.Session()
    user = session.query(db.models.User).filter_by(email=create_task_info.email).first()
    if not user or user.password != create_task_info.password:
        session.close()
        return schemas.ResponseError(error_code=401, description="Invalid email or password")
    active_servers = session.query(db.models.Node).filter_by(status="active").all()
    if not active_servers:
        session.close()
        return schemas.ResponseError(error_code=500, description="Compute servers are not deployed")

    # BALANCING
    server_stats = {server.id: 0 for server in session.query(db.models.Node).filter_by(status="active").all()}
    for task in session.query(db.models.Task).filter_by(status="pending").all():
        server_stats[task.node_id] += 1
    min_loaded_server_id = sorted(server_stats.items(), key=lambda pair: pair[1])[0][0]
    min_loaded_server = session.query(db.models.Node).filter_by(id=min_loaded_server_id).first()
    # ^BALANCING

    async with httpx.AsyncClient() as client:
        response = (await client.post(
            f"http://{min_loaded_server.ip}:{min_loaded_server.port}/createTask",
            json={"user_id": user.id, "input_data": create_task_info.input_data},
        )).json()
    task = session.query(db.models.Task).filter_by(id=response["result"]["task_id"]).first()
    task_info = task.to_schema().dict()
    session.close()
    return schemas.ResponseOK(result={"task": task_info})


@app.get("/getTasks", response_model=schemas.ResponseOK | schemas.ResponseError)
async def get_tasks(user_info: schemas.User):
    session = db.Session()
    #щоб не можна було витягнути інформацію про чужі tasks
    user = session.query(db.models.User).filter_by(email=user_info.email).first()
    if not user or user.password != user_info.password:
        session.close()
        return schemas.ResponseError(erro_code=401, description="Invalid email or password")
    # Пошук усіх завдань для користувача з вказаним user_id
    tasks = session.query(db.models.Task).filter(db.models.Task.user_id == user.id).order_by(db.models.Task.id.desc()).all()
    # Повертання списку задач у вигляді списку словників
    task_list = []
    for task in tasks:
        task_list.append(task.to_schema().dict())
    session.close()
    return schemas.ResponseOK(result={"tasks": task_list})


@app.post("/cancelTask", response_model=schemas.ResponseOK | schemas.ResponseError)
async def cancel_task(cancel_task_info: schemas.CancelTask):
    session = db.Session()
    task = session.query(db.models.Task).filter_by(id=cancel_task_info.task_id).first()
    user = session.query(db.models.User).filter_by(email=cancel_task_info.email).first()
    if not user or user.password != cancel_task_info.password:
        session.close()
        return schemas.ResponseError(error_code=401, description="Invalid email or password")
    if not task:
        return schemas.ResponseError(error_code=404, description="Task not found")
    server = session.query(db.models.Node).filter_by(id=task.node_id).first()
    if task.status != "pending" or task.status == "finished":
        return schemas.ResponseError(error_code=400, description="Task cannot be canceled")
    task.status = "canceled"
    task.progress = 0
    session.commit()
    async with httpx.AsyncClient() as client:
        response = (await client.post(
            f"http://{server.ip}:{server.port}/cancelTask",
            json={"task_id": task.id},
        )).json()
    task_info = task.to_schema().dict()
    session.close()
    return schemas.ResponseOK(result={"task": task_info})



