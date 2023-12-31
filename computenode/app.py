from fastapi import FastAPI, Request, HTTPException
from asyncio import create_task, Task
from colorama import init as colorama_init
from json import dumps
from threading import Thread
from threading import Event

import db
from . import utils
from . import core


class ProxyFastAPI(FastAPI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.proxy = None
        self.ip = None
        self.port = None

    def set_proxy(self, proxy: str):
        self.proxy = proxy

    def set_ip(self, ip: str):
        self.ip = ip

    def set_port(self, port: int):
        self.port = port


colorama_init(autoreset=True)
app = ProxyFastAPI()
# aio_tasks: dict[int: Task] = {}
aio_tasks: dict[int: tuple[Thread, Event]] = {}


def start_task(task: db.models.Task):
    stop_event = Event()
    new_task = Thread(target=core.compute, args=(task.id, stop_event,))
    new_task.start()
    aio_tasks[task.id] = (new_task, stop_event)


@app.on_event("startup")
async def startup():
    session = db.Session()
    node = session.query(db.models.Node).filter_by(ip=app.ip, port=app.port).first()
    if not node:
        node = db.models.Node(
            ip=app.ip,
            port=app.port,
            status="active"
        )
        session.add(node)
    node.status = "active"
    tasks_paused = session.query(db.models.Task).filter_by(node_id=node.id, status="paused")
    for task in tasks_paused:
        task.status = "pending"
        start_task(task)
    session.commit()


@app.on_event("shutdown")
def shutdown():
    session = db.Session()
    node = session.query(db.models.Node).filter_by(ip=app.ip, port=app.port, status="active").first()
    node.status = "inactive"
    tasks = session.query(db.models.Task).filter_by(node_id=node.id, status="pending")
    for task in tasks:
        task.status = "paused"
    session.commit()


@app.get("/status", status_code=200)
async def check_status():
    pass


@app.post("/createTask")
async def compute(request: Request):
    session = db.Session()
    json_data = await request.json()
    user_id = json_data["user_id"]
    input_data = json_data["input_data"]
    if request.client.host not in (app.proxy, "127.0.0.1"):
        return HTTPException(403, "Access denied")
    node = session.query(db.models.Node).filter_by(ip=app.ip, port=app.port).first()
    user = session.query(db.models.User).filter_by(id=user_id).first()
    if not user:
        return HTTPException(404, "User not found")

    if not utils.validate_input_data(input_data):
        return HTTPException(404, f"Invalid input_data")
    task = db.models.Task(
        user_id=user_id,
        node_id=node.id,
        input_data=dumps(input_data)
    )
    session.add(task)
    session.commit()
    start_task(task)
    return {"ok": True, "result": {"task_id": task.id}}


@app.post("/cancelTask", status_code=200)
async def cancel_task(request: Request):
    json_data = await request.json()
    task_id = json_data["task_id"]
    if request.client.host not in (app.proxy, "127.0.0.1"):
        return HTTPException(403, "Access denied")
    session = db.Session()
    task = session.query(db.models.Task).filter_by(id=task_id).first()
    if not task:
        return HTTPException(404, "Task to cancel not found")
    if task_id in aio_tasks.keys():
        aio_tasks[task_id][1].set()
    return {"ok": True}
