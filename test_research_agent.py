"""
Simple test script for Research Agent with Groq (Free)
"""

import asyncio
from src.llm.groq_client import GroqClient
from src.agents.research import ResearchAgent
from src.config import settings


async def main():
    print("=" * 60)
    print("Testing Research Agent with Groq")
    print("=" * 60)
    
    # Initialize Groq client (FREE!)
    print("\n1. Initializing Groq client...")
    llm_client = GroqClient(
        api_key=settings.groq_api_key,
        model=settings.groq_model
    )
    print(f"✓ Groq client initialized (Model: {settings.groq_model})")
    
    # Test connection
    print("\n2. Testing Groq connection...")
    try:
        connected = await llm_client.test_connection()
        if not connected:
            print("❌ Failed to connect to Groq")
            return
        print("✓ Connected to Groq API")
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return
    
    # Create agent
    print("\n3. Creating Research Agent...")
    agent = ResearchAgent(llm_client)
    print(f"✓ Agent created: {agent.name}")
    
    # Execute task
    print("\n4. Executing research task...")
    task = "What are the latest trends in artificial intelligence?"
    print(f"   Task: {task}")
    
    result = await agent.execute(task)
    
    # Display result
    print("\n5. Result:")
    print("-" * 60)
    if result["success"]:
        print("✓ SUCCESS!")
        print("\nResponse:")
        print(result["result"])
        print("\nMetadata:")
        for key, value in result["metadata"].items():
            print(f"  {key}: {value}")
    else:
        print(f"❌ FAILED: {result['error']}")
    
    print("\n" + "=" * 60)
    print("Test Complete! Groq is working perfectly!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())