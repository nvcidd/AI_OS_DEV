from src.agents.planner_agent import PlannerAgent
from src.agents.research_agent import ResearchAgent
from src.agents.summarizer_agent import SummarizerAgent
from src.agents.memory_agent import MemoryAgent


class WorkflowManager:

    def __init__(self):

        self.planner = PlannerAgent()
        self.research = ResearchAgent()
        self.summarizer = SummarizerAgent()
        self.memory = MemoryAgent()

    def execute(self, goal):

        tasks = self.planner.execute(goal)

        research = self.research.execute(goal)

        summary = self.summarizer.execute(
            research
        )

        result = {
            "tasks": tasks,
            "research": research,
            "summary": summary
        }

        self.memory.save(result)

        return result