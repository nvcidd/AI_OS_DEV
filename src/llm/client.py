"""
AI Operating System - LLM Client
OpenAI API wrapper with error handling and rate limiting
"""

import logging
import asyncio
from typing import Optional
from openai import AsyncOpenAI, RateLimitError, APIError
from tenacity import retry, wait_exponential, stop_after_attempt

logger = logging.getLogger(__name__)


class LLMClient:
    """
    Wrapper around OpenAI API with error handling and rate limiting.
    
    Features:
    - Automatic retries with exponential backoff
    - Token counting for cost estimation
    - Error handling and logging
    - Configurable model and parameters
    """
    
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4-turbo-preview",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ):
        """
        Initialize LLM client.
        
        Args:
            api_key: OpenAI API key
            model: Model to use
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens in response
        """
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.logger = logging.getLogger(__name__)
        self.call_count = 0
        self.total_input_tokens = 0
        self.total_output_tokens = 0
    
    @retry(
        wait=wait_exponential(multiplier=1, min=2, max=10),
        stop=stop_after_attempt(3)
    )
    async def generate(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Generate text using OpenAI API with automatic retry logic.
        
        Args:
            prompt: User prompt
            system_message: System context (optional)
            **kwargs: Additional parameters to pass to OpenAI
            
        Returns:
            Generated text
            
        Raises:
            APIError: If API call fails after retries
        """
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            self.logger.info(f"Calling OpenAI API with model: {self.model}")
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                **kwargs
            )
            
            # Track usage
            self.call_count += 1
            self.total_input_tokens += response.usage.prompt_tokens
            self.total_output_tokens += response.usage.completion_tokens
            
            result = response.choices[0].message.content
            
            self.logger.info(
                f"API call succeeded. "
                f"Tokens: {response.usage.prompt_tokens} input, "
                f"{response.usage.completion_tokens} output"
            )
            
            return result
            
        except RateLimitError as e:
            self.logger.error(f"Rate limited by OpenAI API: {e}")
            raise
        except APIError as e:
            self.logger.error(f"OpenAI API error: {e}")
            raise
    
    async def generate_json(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        **kwargs
    ) -> dict:
        """
        Generate JSON response from OpenAI.
        
        Args:
            prompt: User prompt
            system_message: System context
            **kwargs: Additional parameters
            
        Returns:
            Parsed JSON response
            
        Raises:
            ValueError: If response is not valid JSON
        """
        import json
        
        result = await self.generate(
            prompt=prompt,
            system_message=system_message,
            response_format={"type": "json_object"},
            **kwargs
        )
        
        try:
            return json.loads(result)
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON response: {result}")
            raise ValueError(f"Invalid JSON response: {e}")
    
    def get_stats(self) -> dict:
        """Get API usage statistics"""
        return {
            "call_count": self.call_count,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "estimated_cost_usd": self._estimate_cost()
        }
    
    def _estimate_cost(self) -> float:
        """
        Rough cost estimation for API calls.
        Prices as of 2024 - update as needed.
        """
        # GPT-4 Turbo: $0.01 per 1K input tokens, $0.03 per 1K output tokens
        input_cost = (self.total_input_tokens / 1000) * 0.01
        output_cost = (self.total_output_tokens / 1000) * 0.03
        return round(input_cost + output_cost, 4)
    
    async def test_connection(self) -> bool:
        """
        Test API connection with a simple call.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            result = await self.generate("Say 'Hello' and nothing else.")
            self.logger.info("API connection test successful")
            return True
        except Exception as e:
            self.logger.error(f"API connection test failed: {e}")
            return False


class PromptTemplate:
    """
    Simple prompt template manager for consistent prompt engineering.
    """
    
    @staticmethod
    def research_prompt(query: str) -> tuple[str, str]:
        """Return (system_message, user_prompt) for research agent"""
        system = """You are a research expert. Provide accurate, 
        well-researched information on the requested topic. 
        Structure your response clearly with key findings."""
        
        user = f"Research the following topic and provide a comprehensive summary: {query}"
        
        return system, user
    
    @staticmethod
    def code_generation_prompt(request: str) -> tuple[str, str]:
        """Return (system_message, user_prompt) for code generation"""
        system = """You are an expert Python developer. Write clean, 
        well-documented, production-ready code. Include docstrings and type hints. 
        Explain your approach."""
        
        user = f"Write Python code for: {request}"
        
        return system, user
    
    @staticmethod
    def summary_prompt(text: str) -> tuple[str, str]:
        """Return (system_message, user_prompt) for summary agent"""
        system = """You are a concise summarization expert. 
        Provide clear, well-structured summaries that capture key points."""
        
        user = f"Summarize the following text:\n\n{text}"
        
        return system, user
