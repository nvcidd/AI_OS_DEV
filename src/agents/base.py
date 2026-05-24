from src.llm.groq_client import GroqClient


class BaseAgent:

    def __init__(self):

        self.llm = GroqClient()

    def execute(self, task):

        raise NotImplementedError()