from src.router.task_router import TaskRouter

router = TaskRouter()

result1 = router.route(
    "Research AI trends"
)

result2 = router.route(
    "Summarize this article"
)

print(result1)
print(result2)