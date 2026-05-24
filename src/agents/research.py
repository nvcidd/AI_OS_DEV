"""
Research Agent - Uses LLM to search and summarize information
"""

import time
import asyncio
from typing import Dict, Any
from src.agents.base import Agent, get_registry
from src.llm.client import LLMClient, PromptTemplate


@get_registry().register("research")
class ResearchAgent(Agent):
    """Agent that searches and summarizes information"""
    
    name = "ResearchAgent"
    description = "Searches and summarizes information"
    supported_task_types = ["research"]
    
    def __init__(self, llm_client: LLMClient):
        super().__init__()
        self.llm_client = llm_client
    
    async def execute(
        self,
        task_description: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Execute research task"""
        start_time = time.time()
        
        try:
            # Validate input
            if not self.validate_input(task_description):
                return {
                    "success": False,
                    "result": None,
                    "error": "Invalid input"
                }
            
            # Get prompt template
            system_msg, user_prompt = PromptTemplate.research_prompt(task_description)
            
            # Log execution
            self.logger.info(f"Executing research: {task_description[:50]}...")
            
            # Call LLM
            result = await self.llm_client.generate(user_prompt, system_msg)
            
            # Calculate execution time
            execution_time = time.time() - start_time
            
            # Return result
            return {
                "success": True,
                "result": result,
                "metadata": {
                    "execution_time_seconds": round(execution_time, 2),
                    "agent": self.name,
                    "model": self.llm_client.model
                }
            }
        
        except Exception as e:
            self.logger.error(f"Research execution failed: {e}")
            return {
                "success": False,
                "result": None,
                "error": str(e)
            }