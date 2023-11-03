from fastapi import FastAPI, Request, HTTPException
from asyncio import create_task, Task
from json import dumps
import httpx

import db

app = FastAPI()


@app.post("/registration")
async def registration(request: Request):
    session = db.Session()
    json_data = await request.json()
    email = json_data["email"]
    password = json_data["password"]
    existing_user = session.query(db.models.User).filter_by(email=email).first()
    if existing_user:
        session.close()
        return HTTPException(409, "User with this email already exists")
    if len(password) < 8:
        session.close()
        return HTTPException(400, "Password is too weak")
    new_user = db.models.User(email=email, password=password)
    session.add(new_user)
    session.commit()
    session.close()
    return {"message": "User registered successfully"}


@app.post("/signin")
async def signin(request: Request):
    session = db.Session()
    json_data = await request.json()
    email = json_data["email"]
    password = json_data["password"]
    user = session.query(db.models.User).filter_by(email=email).first()
    if not user or user.password != password:
        session.close()
        return HTTPException(401, "Invalid email or password")
    session.close()
    return {"message": "User signed in successfully"}


@app.post("/createTask")
async def compute(request: Request):
    session = db.Session()
    json_data = await request.json()
    email = json_data["email"]
    password = json_data["password"]
    input_data = json_data["input_data"]
    user = session.query(db.models.User).filter_by(email=email).first()
    if not user or user.password != password:
        session.close()
        return HTTPException(401, "Invalid email or password")
    try:
        number = int(input_data)
    except ValueError:
        return HTTPException(401, "Це не число")
    if number <= 0:
        return HTTPException(401, "Це не додатнє число")

    active_servers = session.query(db.models.Node).filter_by(status="active").all()
    min_loaded_server = active_servers[0]

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://{min_loaded_server.ip}:{min_loaded_server.port}/createTask",
            json={"user_id": user.id, "input_data": input_data},
        )
    return "OK"


@app.get("/user_tasks/{user_id}")
async def get_user_tasks(request: Request):
    session = db.Session()
    json_data = await request.json()
    email = json_data["email"]
    password = json_data["password"]
    #щоб не можна було витягнути інформацію про чужі tasks
    user = session.query(db.models.User).filter_by(email=email).first()
    if not user or user.password != password:
        session.close()
        return HTTPException(401, "Invalid email or password")
    # Пошук усіх завдань для користувача з вказаним user_id
    tasks = session.query(db.models.Task).filter(db.models.Task.user_id == user.id).all()

    session.close()
    # Повертання списку задач у вигляді списку словників
    task_list = []
    for task in tasks:
        task_dict = {
            "id": task.id,
            "user_id": task.user_id,
            "node_id": task.node_id,
            "status": task.status,
            "error": task.error,
            "progress": task.progress,
            "input_data": task.input_data,
            "output_data": task.output_data
        }
        task_list.append(task_dict)
    return task_list
