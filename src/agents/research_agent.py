from src.agents.base import BaseAgent


class ResearchAgent(BaseAgent):

    def execute(self, topic):

        prompt = f"""
        Research the following topic and provide
        detailed information:

        Topic:
        {topic}
        """

        response = self.llm.generate(
            prompt
        )

        return response