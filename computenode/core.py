from asyncio import sleep, CancelledError
from json import dumps
import db


async def compute(task_id: int):
    session = db.Session()
    task = session.query(db.models.Task).filter_by(id=task_id).first()
    try:
        match task.method:
            case "SLAEbyIterations":
                output_data = await SLAEbyIterations(task.get_input_data())
            case _:
                raise ValueError()
    except CancelledError:
        return
    task.output_data = dumps(output_data)
    task.status = "finished"
    task.progress = 100
    session.commit()


async def SLAEbyIterations(input_data: list[list[float]]) -> list[float]:
    await sleep(50)
    return input_data[0]