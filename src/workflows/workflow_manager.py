from src.agents.planner_agent import PlannerAgent


class WorkflowManager:

    def __init__(self):

        self.planner = PlannerAgent()


    def execute(self, user_goal):

        tasks = self.planner.execute(
            user_goal
        )

        return tasks