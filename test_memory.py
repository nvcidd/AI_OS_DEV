from src.workflows.workflow_manager import WorkflowManager

manager=WorkflowManager()

manager.execute(
    "Research AI trends"
)

print(
    manager.memory.get_memory()
)