from threading import Event
from json import dumps
import db
import random
import time
from . import exceptions


def compute(task_id: int, stop_event: Event):
    session = db.Session()
    task = session.query(db.models.Task).filter_by(id=task_id).first()
    input_data = task.get_input_data()
    size_value = input_data
    try:
        output_data = SLAEbyIterations(size_value, stop_event, task, session)
    except exceptions.CancelledError:
        task.status = "cancelled"
        session.commit()
        return
    except Exception as exc:
        task.error = f"{type(exc).__name__}: {exc}"
        task.progress = 0
        task.status = "error"
        session.commit()
        return
    task.output_data = dumps(output_data)
    task.status = "finished"
    task.progress = 100
    session.commit()


def SLAEbyIterations(input_data: int, stop_event: Event, task: db.models.Task, session):
    if input_data <= 2:
        exceptions.Error("not valid size")
    matrix, right_column = fillRandomSLAR(input_data)

    N = len(matrix)
    result = [0] * N
    start_time = time.time()
    # a1 = N-1
    # d = 1
    total_iter_num = int((N-1)*N)
    progress = 0
    for i in range(N):
        for j in range(i + 1, N):
            if stop_event.is_set():
                raise exceptions.CancelledError()
            mnj = matrix[j][i] / matrix[i][i]
            for k in range(i, N):
                matrix[j][k] -= mnj * matrix[i][k]
            right_column[j] -= mnj * right_column[i]
            progress += 1
            if int(progress/total_iter_num*100) - task.progress > 5:
                task.progress = int(progress/total_iter_num*100)
                session.commit()
    for i in range(N - 1, -1, -1):
        result[i] = right_column[i]
        for j in range(i + 1, N):
            if stop_event.is_set():
                raise exceptions.CancelledError()
            result[i] -= matrix[i][j] * result[j]
            progress += 1
            if int(progress/total_iter_num*100) - task.progress > 5:
                task.progress = int(progress/total_iter_num*100)
                session.commit()
        result[i] /= matrix[i][i]
    end_time = time.time()
    return result


def fillRandomSLAR(size):
    matrix = [[random.randint(1, 20) for _ in range(size)] for _ in range(size)]
    right_column = [random.randint(1, 20) for _ in range(size)]
    return matrix, right_column
