from src.router.task_router import TaskRouter
from src.agents.registry import AgentRegistry

from src.agents.research_agent import ResearchAgent
from src.agents.planner_agent import PlannerAgent
from src.agents.summarizer_agent import SummarizerAgent


class TaskExecutor:

    def __init__(self):

        self.router = TaskRouter()

        self.registry = AgentRegistry()

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

    def execute(self, user_input):

        agent_name = self.router.route(
            user_input
        )

        agent = self.registry.get(
            agent_name
        )

        return agent.execute(
            user_input
        )