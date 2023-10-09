from asyncio import sleep, CancelledError
from json import dumps
import db
from . import exceptions


async def compute(task_id: int):
    session = db.Session()
    task = session.query(db.models.Task).filter_by(id=task_id).first()
    try:
        output_data = await SLAEbyIterations(task.get_input_data())
    except CancelledError:
        print("CancelledError")
        return
    except exceptions.ExceptionError as exc:
        print("[-----------")
        task.error= f"{type(exc).__name__}: {exc}"
        task.progress=0
        task.status="error"
        session.commit()
        print(" ecxeption Error")
        return
    print(" finishing")
    task.output_data = dumps(output_data)
    task.status = "finished"
    task.progress = 100
    session.commit()


async def SLAEbyIterations(input_data: list[list[float]]) -> list[float]:
    await sleep(20)
    print("before exeotion")
    raise exceptions.ExceptionError()
    print("after exeption")
    return input_data[0]