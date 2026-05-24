"""
AI Operating System - Base Agent Architecture
Abstract base class and registry pattern for agents
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Type
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class Agent(ABC):
    """
    Abstract base class for all agents.
    
    Agents are specialized task handlers that can execute specific types of tasks.
    New agents should inherit from this class and implement execute() method.
    
    Example:
        class ResearchAgent(Agent):
            name = "ResearchAgent"
            description = "Searches and summarizes information"
            supported_task_types = ["research"]
            
            def execute(self, task_description: str, **kwargs) -> Dict[str, Any]:
                # Implementation here
                return {"result": "..."}
    """
    
    name: str  # Unique agent identifier
    description: str  # Human-readable description
    version: str = "0.1.0"
    supported_task_types: list[str] = []  # e.g., ["research", "summarization"]
    
    def __init__(self):
        """Initialize agent"""
        self.logger = logging.getLogger(self.__class__.__name__)
        self.execution_count = 0
        self.total_execution_time = 0.0
    
    @abstractmethod
    async def execute(
        self,
        task_description: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute a task using this agent.
        
        Args:
            task_description: Natural language description of what to do
            **kwargs: Additional context or parameters
            
        Returns:
            Dictionary with at minimum:
            - "success": bool
            - "result": str or dict (the actual output)
            - "metadata": dict (execution details)
            
        Raises:
            AgentExecutionError: If execution fails
        """
        pass
    
    def validate_input(self, task_description: str) -> bool:
        """
        Validate that input is appropriate for this agent.
        Override to add custom validation.
        """
        if not task_description or len(task_description) == 0:
            self.logger.warning("Empty task description")
            return False
        if len(task_description) > 5000:
            self.logger.warning("Task description too long")
            return False
        return True
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} v{self.version}>"


class AgentRegistry:
    """
    Registry pattern for agents.
    
    Allows dynamic registration and lookup of agents.
    This enables adding new agents without modifying core code.
    
    Usage:
        registry = AgentRegistry()
        
        @registry.register("research")
        class ResearchAgent(Agent):
            ...
        
        # Later
        agent = registry.get("research")
        result = await agent.execute("Search for X")
    """
    
    def __init__(self):
        """Initialize agent registry"""
        self._agents: Dict[str, Type[Agent]] = {}
        self._instances: Dict[str, Agent] = {}
        self.logger = logging.getLogger(__name__)
    
    def register(self, task_type: str):
        """
        Decorator to register an agent.
        
        Args:
            task_type: The task type this agent handles
            
        Usage:
            @registry.register("research")
            class ResearchAgent(Agent):
                ...
        """
        def decorator(agent_class: Type[Agent]) -> Type[Agent]:
            if task_type in self._agents:
                self.logger.warning(
                    f"Overwriting existing agent for task_type: {task_type}"
                )
            self._agents[task_type] = agent_class
            self.logger.info(
                f"Registered agent {agent_class.__name__} for task_type: {task_type}"
            )
            return agent_class
        return decorator
    
    def register_instance(self, task_type: str, agent_instance: Agent) -> None:
        """
        Register an agent instance directly.
        
        Args:
            task_type: The task type this agent handles
            agent_instance: An instance of an Agent
        """
        self._agents[task_type] = agent_instance.__class__
        self._instances[task_type] = agent_instance
        self.logger.info(
            f"Registered instance of {agent_instance.__class__.__name__} "
            f"for task_type: {task_type}"
        )
    
    def get(self, task_type: str) -> Optional[Agent]:
        """
        Get agent instance for a task type.
        
        Args:
            task_type: The task type to get agent for
            
        Returns:
            Agent instance or None if not found
        """
        if task_type not in self._agents:
            self.logger.warning(f"No agent registered for task_type: {task_type}")
            return None
        
        # Return cached instance if available
        if task_type in self._instances:
            return self._instances[task_type]
        
        # Create new instance
        agent_class = self._agents[task_type]
        agent_instance = agent_class()
        self._instances[task_type] = agent_instance
        return agent_instance
    
    def list_agents(self) -> Dict[str, str]:
        """
        List all registered agents.
        
        Returns:
            Dictionary of {task_type: agent_name}
        """
        return {
            task_type: agent_class.__name__
            for task_type, agent_class in self._agents.items()
        }
    
    def is_registered(self, task_type: str) -> bool:
        """Check if agent is registered for task type"""
        return task_type in self._agents


class AgentExecutionError(Exception):
    """Raised when agent execution fails"""
    pass


# Global registry instance
_registry = AgentRegistry()


def get_registry() -> AgentRegistry:
    """Get the global agent registry"""
    return _registry
