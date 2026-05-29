from fastapi import FastAPI

from src.executor.executor import TaskExecutor

app = FastAPI()

executor = TaskExecutor()


@app.get("/")
def home():

    return {
        "message": "DevMind AI Operating System"
    }


@app.post("/task")
def run_task(task: str):

    result = executor.execute(task)

    return {
        "task": task,
        "result": result
    }