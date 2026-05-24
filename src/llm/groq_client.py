import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class GroqClient:

    def __init__(self):

        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv("GROQ_MODEL")

        self.client = Groq(
            api_key=self.api_key
        )

    def generate(self, prompt):

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content