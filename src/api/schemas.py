from pydantic import BaseModel


class TaskRequest(BaseModel):

    task: str


class TaskResponse(BaseModel):

    task: str

    status: str

    result: str