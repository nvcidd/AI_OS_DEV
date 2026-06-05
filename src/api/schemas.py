from pydantic import BaseModel


class TaskRequest(BaseModel):

    task: str


class TaskResponse(BaseModel):

    task_id: int

    task: str

    status: str