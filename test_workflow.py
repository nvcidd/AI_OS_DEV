from src.workflows.workflow_manager import WorkflowManager

manager = WorkflowManager()

result = manager.execute(
    "Research AI trends and summarize"
)

print(result)