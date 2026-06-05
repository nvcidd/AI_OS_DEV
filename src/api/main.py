from fastapi import FastAPI
from src.workers.background_worker import BackgroundWorker
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


@app.post("/task")
def run_task(
    request: TaskRequest
):

    task_id = executor.db.create_task(
        request.task
    )

    BackgroundWorker.run(

        executor.execute_async,

        task_id,

        request.task
    )

    return {

        "task_id": task_id,

        "task": request.task,

        "status": "PENDING"
    }

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

    return {

        "tasks": formatted_tasks

    }

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

