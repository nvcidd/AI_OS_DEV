# 🚀 Quick Start Guide - AI Operating System

## 5-Minute Setup

### 1. Clone and Setup Environment
```bash
# Create project directory
mkdir ai-operating-system
cd ai-operating-system

# Initialize git
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Create folder structure
mkdir src src/agents src/llm src/api src/router src/executor tests docs
touch src/__init__.py
```

### 2. Install Dependencies
```bash
# Copy the requirements.txt provided
pip install -r requirements.txt
```

### 3. Setup Environment Variables
```bash
# Create .env file
cat > .env << EOF
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4-turbo-preview
DATABASE_URL=sqlite:///./ai_os.db
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
EOF
```

**Get API key from:** https://platform.openai.com/api-keys

### 4. First Commit
```bash
git add .
git commit -m "init: project scaffold with folder structure"
```

---

## Your First Agent (30 minutes)

### Create Base Agent Class
**File: `src/agents/base.py`**
- Copy content from `src_agents_base.py` provided
- Commit: `feat: abstract agent pattern and registry`

### Create LLM Client
**File: `src/llm/client.py`**
- Copy content from `src_llm_client.py` provided
- Commit: `feat: openai integration with error handling`

### Create Your First Agent - Research Agent
**File: `src/agents/research.py`**
```python
from src.agents.base import Agent, get_registry
from src.llm.client import LLMClient, PromptTemplate
from typing import Dict, Any
import time

@get_registry().register("research")
class ResearchAgent(Agent):
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
            if not self.validate_input(task_description):
                return {
                    "success": False,
                    "result": None,
                    "error": "Invalid input"
                }
            
            # Get prompt
            system_msg, user_prompt = PromptTemplate.research_prompt(task_description)
            
            # Call LLM
            self.logger.info(f"Executing research: {task_description[:50]}...")
            result = await self.llm_client.generate(user_prompt, system_msg)
            
            execution_time = time.time() - start_time
            
            return {
                "success": True,
                "result": result,
                "metadata": {
                    "execution_time_seconds": execution_time,
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
```

Commit: `feat: research agent with web search capability`

### Test It
**File: `tests/test_agents.py`**
```python
import pytest
from unittest.mock import AsyncMock, patch
from src.agents.research import ResearchAgent
from src.llm.client import LLMClient


@pytest.mark.asyncio
async def test_research_agent_executes():
    """Test research agent can execute"""
    mock_llm = AsyncMock(spec=LLMClient)
    mock_llm.generate = AsyncMock(return_value="Research results here")
    
    agent = ResearchAgent(mock_llm)
    result = await agent.execute("AI trends 2024")
    
    assert result["success"] is True
    assert "Research results" in result["result"]


@pytest.mark.asyncio
async def test_research_agent_handles_empty_input():
    """Test agent validates empty input"""
    mock_llm = AsyncMock(spec=LLMClient)
    agent = ResearchAgent(mock_llm)
    
    result = await agent.execute("")
    assert result["success"] is False
```

Run tests:
```bash
pytest tests/test_agents.py -v
```

Commit: `test: unit tests for research agent`

---

## Create Simple API Endpoint (20 minutes)

**File: `src/api/main.py`**
```python
from fastapi import FastAPI, HTTPException
from src.models import TaskCreate, TaskResponse, TaskStatus, TaskORM
from src.agents.research import ResearchAgent
from src.llm.client import LLMClient
from src.config import settings
import asyncio
from datetime import datetime

app = FastAPI(
    title=settings.api_title,
    version=settings.api_version
)

# Initialize LLM and agents
llm_client = LLMClient(
    api_key=settings.openai_api_key,
    model=settings.openai_model
)

research_agent = ResearchAgent(llm_client)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": settings.api_version}

@app.post("/tasks")
async def create_task(task: TaskCreate) -> TaskResponse:
    """Create and execute a task"""
    try:
        # Route to appropriate agent
        if "search" in task.description.lower():
            result = await research_agent.execute(task.description)
        else:
            return {"error": "Task type not supported"}, 400
        
        # Return response
        return TaskResponse(
            id="task-1",
            description=task.description,
            status=TaskStatus.COMPLETED,
            task_type="research",
            result=result.get("result"),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)
```

Commit: `feat: fastapi endpoints for task management`

### Test API Locally
```bash
# Start server
python -m uvicorn src.api.main:app --reload

# In another terminal
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"description": "Search for Python best practices"}'
```

---

## CLI Interface (15 minutes)

**File: `src/cli/main.py`**
```python
import typer
import asyncio
from src.agents.research import ResearchAgent
from src.llm.client import LLMClient
from src.config import settings

app = typer.Typer()

llm_client = LLMClient(
    api_key=settings.openai_api_key,
    model=settings.openai_model
)

research_agent = ResearchAgent(llm_client)

@app.command()
def execute(description: str):
    """Execute a task"""
    typer.echo(f"Executing: {description}")
    
    result = asyncio.run(research_agent.execute(description))
    
    if result["success"]:
        typer.echo(f"\n✅ Success!")
        typer.echo(f"\nResult:\n{result['result']}")
    else:
        typer.echo(f"\n❌ Failed: {result.get('error')}")

if __name__ == "__main__":
    app()
```

Test it:
```bash
python -m src.cli.main execute "Search for AI trends in 2024"
```

Commit: `feat: cli interface with typer`

---

## Git Commit Checklist for Week 1

```bash
# By end of Week 1, you should have these commits:
git log --oneline

# Should show:
# feat: abstract agent pattern and registry
# feat: openai integration with error handling
# feat: research agent with web search capability
# test: unit tests for research agent
# feat: fastapi endpoints for task management
# feat: cli interface with typer
# init: project scaffold with folder structure
```

---

## Next Steps

1. **Week 2**: Create 2 more agents (Code, Summary)
2. **Week 3**: Build task router (intelligent routing)
3. **Week 4-5**: API enhancements, database integration
4. **Week 6-7**: Deployment, documentation
5. **Week 8**: Interview prep

---

## Debugging Tips

### Issue: "ModuleNotFoundError"
```bash
# Make sure you're in project root and venv is activated
python -c "import src; print(src.__file__)"
```

### Issue: OpenAI API errors
```python
# Add this to test connection
import asyncio
from src.llm.client import LLMClient
from src.config import settings

async def test():
    client = LLMClient(settings.openai_api_key)
    result = await client.test_connection()
    print("Connected!" if result else "Failed!")

asyncio.run(test())
```

### Issue: Database errors
```bash
# Reset SQLite database
rm ai_os.db
python src/database.py  # Creates fresh schema
```

---

## Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **OpenAI API**: https://platform.openai.com/docs/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Pydantic**: https://docs.pydantic.dev/

---

**You're now ready to start! Begin with Week 1 and commit daily.** 🚀
