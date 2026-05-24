from src.agents.base import BaseAgent


class SummarizerAgent(BaseAgent):

    def execute(self, text):

        prompt = f"""
        Summarize the following content
        into concise bullet points:

        {text}
        """

        response = self.llm.generate(
            prompt
        )

        return response