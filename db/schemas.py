from pydantic import BaseModel, PositiveInt, NonNegativeInt


class User(BaseModel):
    email: str
    password: str


class Task(BaseModel):
    id: PositiveInt
    status: str
    error: str | None
    progress: NonNegativeInt
    input_data: str
    output_data: str | None


class CreateTask(BaseModel):
    email: str
    password: str
    input_data: PositiveInt


class CancelTask(BaseModel):
    email: str
    password: str
    task_id: PositiveInt


class ResponseOK(BaseModel):
    ok: bool = True
    result: dict | None


class ResponseError(BaseModel):
    ok: bool = False
    error_code: int
    description: str
