from fastapi import FastAPI

from src.executor.executor import TaskExecutor
from src.api.schemas import (
    TaskRequest,
    TaskResponse
)

app = FastAPI()

executor = TaskExecutor()


@app.get("/")
def home():

    return {
        "message": "DevMind AI Operating System"
    }


@app.post(
    "/task",
    response_model=TaskResponse
)
def run_task(
    request: TaskRequest
):

    result = executor.execute(
        request.task
    )

    return TaskResponse(
        task=request.task,
        status="COMPLETED",
        result=str(result)
    )


@app.get("/history")
def history():

    tasks = executor.db.get_tasks()

    formatted_tasks = []

    for task in tasks:

        formatted_tasks.append({

            "id": task[0],

            "task": task[1],

            "status": task[2],

            "result": task[3],

            "created_at": task[4]

        })

    return formatted_tasks