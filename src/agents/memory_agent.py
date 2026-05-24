from src.agents.base import BaseAgent


class MemoryAgent(BaseAgent):

    def __init__(self):

        super().__init__()

        self.memory=[]


    def save(self,data):

        self.memory.append(data)


    def get_memory(self):

        return self.memory