from asyncio import sleep, CancelledError
from json import dumps
import db
import random
import time
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


async def SLAEbyIterations(input_data: int):
    if input_data<=2:
        exceptions.ExceptionError("not valid size")
    matrix, right_column = fillRandomSLAR(input_data)
    result1, time1 = poslidovnuy(matrix, right_column)
    return  time1,  result1



def fillRandomSLAR(size):
    matrix = [[random.randint(1, 20) for _ in range(size)] for _ in range(size)]
    right_column = [random.randint(1, 20) for _ in range(size)]
    return matrix, right_column

def poslidovnuy(matrix, right_column):
    N = len(matrix)
    result = [0] * N
    start_time = time.time()

    for i in range(N):
        for j in range(i + 1, N):
            mnj = matrix[j][i] / matrix[i][i]
            for k in range(i, N):
                matrix[j][k] -= mnj * matrix[i][k]
            right_column[j] -= mnj * right_column[i]

    for i in range(N - 1, -1, -1):
        result[i] = right_column[i]
        for j in range(i + 1, N):
            result[i] -= matrix[i][j] * result[j]
        result[i] /= matrix[i][i]

    end_time = time.time()
    return result, (end_time - start_time) * 1000

