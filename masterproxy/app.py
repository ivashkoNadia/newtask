from fastapi import FastAPI, Request, HTTPException
from asyncio import create_task, Task
from json import dumps
import httpx



import db

app = FastAPI()

@app.post("/registration")
async def registration(request: Request):
    print("in registration")
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

    active_servers = session.query(db.models.Node).filter(db.models.Node.status == 'running').all()
    #активні задачі для кожного сервера
    tasks_by_server = {}
    for server in active_servers:
        tasks = (
            session.query(Task)
            .filter(Task.node_id == server.id, Task.status == 'running')
            .all()
        )
        tasks_by_server[server] = tasks

    #пошук найменш завантаженого серверу
    min_load_server = None
    min_progress = float('inf')  # початкове значення "нескінченність"

    for server, tasks in tasks_by_server.items():
        total_progress = sum(task.progress for task in tasks)
        if total_progress < min_progress:
            min_progress = total_progress
            min_load_server = server

    #відправка запиту createTask на цей сервер з вибраними вхідними даними
    create_task_url = f"не знаю як тут точно має бути"

    #вхідні дані
    data = {"email": email, "password": password, "input_data": input_data}

    async with httpx.AsyncClient() as client:
        response = await client.post(create_task_url, json=data)

    # Перевірка результату відповіді
    if response.status_code == 200:
        return "Запит на створення завдання успішно відправлено"
    else:
        return f"Помилка при створенні завдання: {response.status_code}"


@app.get("/user_tasks/{user_id}")
async def get_user_tasks(request: Request):
    print("zero")
    session = db.Session()
    json_data = await request.json()
    email = json_data["email"]
    password = json_data["password"]
    #щоб не можна було витягнути інформацію про чужі tasks
    user = session.query(db.models.User).filter_by(email=email).first()
    if not user or user.password != password:
        session.close()
        return HTTPException(401, "Invalid email or password")
    print("first")

    # Пошук усіх завдань для користувача з вказаним user_id
    tasks = session.query(db.models.Task).filter(db.models.Task.user_id == user.id).all()

    session.close()

    if not tasks:
        return HTTPException(404, "User has no tasks")
    print("second")

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
    print("third")

    return task_list