"""
AI Operating System - Core Models
Pydantic models for API and SQLAlchemy ORM models for database
"""

from pydantic import BaseModel, Field
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, Text, Integer
from sqlalchemy.orm import declarative_base
from datetime import datetime
from enum import Enum
from typing import Optional, Any, Dict
import uuid

# ============================================================================
# ENUMS
# ============================================================================

class TaskStatus(str, Enum):
    """Task execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskType(str, Enum):
    """Types of tasks the system can handle"""
    RESEARCH = "research"
    CODE_GENERATION = "code"
    SUMMARY = "summary"
    GENERAL = "general"


# ============================================================================
# PYDANTIC MODELS (API)
# ============================================================================

class TaskCreate(BaseModel):
    """Create a new task request"""
    description: str = Field(..., min_length=1, max_length=5000)
    priority: int = Field(default=1, ge=1, le=10)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    class Config:
        json_schema_extra = {
            "example": {
                "description": "Search for the latest AI trends in 2024",
                "priority": 5,
                "metadata": {"source": "user_cli"}
            }
        }


class TaskResponse(BaseModel):
    """Task response model"""
    id: str
    description: str
    status: TaskStatus
    task_type: Optional[TaskType]
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    execution_time_seconds: Optional[float] = None

    class Config:
        from_attributes = True


class TaskHistoryResponse(BaseModel):
    """List of tasks"""
    tasks: list[TaskResponse]
    total: int
    page: int
    page_size: int


# ============================================================================
# SQLALCHEMY MODELS (DATABASE)
# ============================================================================

Base = declarative_base()


class TaskORM(Base):
    """Task database model"""
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    description = Column(String(5000), nullable=False)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    task_type = Column(SQLEnum(TaskType), nullable=True)
    
    # Execution details
    result = Column(Text, nullable=True)  # JSON string
    error = Column(Text, nullable=True)
    execution_time_seconds = Column(Integer, nullable=True)
    
    # Priority and metadata
    priority = Column(Integer, default=1)
    metadata = Column(Text, nullable=True)  # JSON string
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Task id={self.id} status={self.status} type={self.task_type}>"


class ExecutionLogORM(Base):
    """Execution log for debugging and monitoring"""
    __tablename__ = "execution_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id = Column(String, nullable=False)  # Foreign key to tasks.id
    
    # Log details
    level = Column(String(10), nullable=False)  # DEBUG, INFO, WARNING, ERROR
    message = Column(Text, nullable=False)
    context = Column(Text, nullable=True)  # JSON string
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<ExecutionLog task_id={self.task_id} level={self.level}>"


# ============================================================================
# AGENT MODELS
# ============================================================================

class AgentDefinition(BaseModel):
    """Definition of an AI Agent"""
    name: str
    description: str
    task_types: list[TaskType]
    version: str = "0.1.0"
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "ResearchAgent",
                "description": "Searches and summarizes information from the web",
                "task_types": ["research"],
                "version": "0.1.0"
            }
        }


class AgentExecution(BaseModel):
    """Record of agent execution"""
    task_id: str
    agent_name: str
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]] = None
    execution_time_seconds: float
    success: bool
    error_message: Optional[str] = None


# ============================================================================
# STATS/MONITORING
# ============================================================================

class SystemStats(BaseModel):
    """System statistics for monitoring"""
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    running_tasks: int
    success_rate: float
    avg_execution_time_seconds: float
    tasks_by_type: Dict[str, int]
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_tasks": 150,
                "completed_tasks": 145,
                "failed_tasks": 5,
                "running_tasks": 0,
                "success_rate": 96.7,
                "avg_execution_time_seconds": 12.5,
                "tasks_by_type": {"research": 50, "code": 75, "summary": 25}
            }
        }
