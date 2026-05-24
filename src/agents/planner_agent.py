from src.agents.base import BaseAgent


class PlannerAgent(BaseAgent):

    def execute(self, goal):

        prompt = f"""
        Break the following goal into
        clear actionable tasks:

        Goal:
        {goal}

        Return only numbered tasks.
        """

        response = self.llm.generate(prompt)

        return response