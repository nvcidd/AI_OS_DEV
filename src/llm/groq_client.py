"""
Groq LLM Client - Free alternative to OpenAI
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class GroqClient:
    """Groq API client for free LLM access"""
    
    def __init__(
        self,
        api_key: str,
        model: str = "llama-3.1-70b-versatile"
    ):
        """Initialize Groq client"""
        from groq import Groq
        
        self.client = Groq(api_key=api_key)
        self.model = model
        self.call_count = 0
        self.logger = logging.getLogger(__name__)
    
    async def generate(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        **kwargs
    ) -> str:
        """Generate text using Groq API"""
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=2000,
                **kwargs
            )
            
            self.call_count += 1
            result = response.choices[0].message.content
            return result
            
        except Exception as e:
            self.logger.error(f"Groq API error: {e}")
            raise
    
    async def test_connection(self) -> bool:
        """Test API connection"""
        try:
            result = await self.generate("Say hello")
            return True
        except Exception as e:
            self.logger.error(f"Connection test failed: {e}")
            return False