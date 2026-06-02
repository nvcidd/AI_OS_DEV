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

@app.get("/tasks/{task_id}")
def get_task(
    task_id: int
):

    task = executor.db.get_task_by_id(
        task_id
    )

    if not task:

        return {
            "error": "Task not found"
        }

    return {

        "id": task[0],

        "task": task[1],

        "status": task[2],

        "result": task[3],

        "created_at": task[4]
    }


@app.get("/metrics")
def metrics():

    return executor.metrics.get_metrics()


@app.get("/analytics")
def analytics():

    return {

        "total_tasks": executor.db.get_total_tasks(),

        "completed_tasks": executor.db.get_completed_tasks(),

        "failed_tasks": (

            executor.db.get_total_tasks()

            -

            executor.db.get_completed_tasks()
        )
    }