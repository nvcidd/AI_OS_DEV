class AgentMetrics:

    def __init__(self):

        self.metrics = {

            "research": 0,

            "planner": 0,

            "summarizer": 0
        }

    def increment(
        self,
        agent_name
    ):

        if agent_name in self.metrics:

            self.metrics[agent_name] += 1

    def get_metrics(self):

        return self.metrics