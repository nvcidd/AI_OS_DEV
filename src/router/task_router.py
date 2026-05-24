class TaskRouter:

    def route(self, user_input):

        text = user_input.lower()

        if "research" in text:
            return "research"

        elif "summarize" in text:
            return "summarizer"

        elif "plan" in text:
            return "planner"

        return "research"