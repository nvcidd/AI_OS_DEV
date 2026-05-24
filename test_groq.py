import os
from dotenv import load_dotenv
from groq import Groq

# Load .env file
load_dotenv()

# Get values from .env
api_key = os.getenv("GROQ_API_KEY")
model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

if not api_key:
    print("❌ GROQ_API_KEY not found")
    exit(1)

print("✓ API key found")
print(f"✓ Model: {model}")

try:
    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": "Say hello"
            }
        ]
    )

    print("✓ Connection successful!")
    print("Response:")
    print(response.choices[0].message.content)

except Exception as e:
    print(f"❌ Error: {e}")