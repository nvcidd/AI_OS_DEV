from src.router.task_router import TaskRouter
from src.agents.registry import AgentRegistry

from src.agents.research_agent import ResearchAgent
from src.agents.planner_agent import PlannerAgent
from src.agents.summarizer_agent import SummarizerAgent
from src.metrics.agent_metrics import AgentMetrics
from src.database import Database


class TaskExecutor:

    def __init__(self):
       

        self.router = TaskRouter()

        self.registry = AgentRegistry()

        self.db = Database()

        self.metrics = AgentMetrics()

        self.registry.register(
            "research",
            ResearchAgent()
        )

        self.registry.register(
            "planner",
            PlannerAgent()
        )

        self.registry.register(
            "summarizer",
            SummarizerAgent()
        )

    def execute(
        self,
        user_input
    ):

        task_id = self.db.create_task(
            user_input
        )

        self.db.update_task_status(
            task_id,
            "RUNNING"
        )

        agent_name = self.router.route(
            user_input
        )

        self.metrics.increment(
            agent_name
        )

        agent = self.registry.get(
            agent_name
        )

        result = agent.execute(
            user_input
        )

        self.db.complete_task(
            task_id,
            result
        )

        return result