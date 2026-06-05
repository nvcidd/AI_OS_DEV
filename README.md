# DevMind AI Operating System

A multi-agent AI workflow platform built using FastAPI, Streamlit, SQLite, Docker, and Groq LLM.

## Features

### Multi-Agent Architecture

* Research Agent
* Planner Agent
* Summarizer Agent

### Task Management

* Asynchronous task execution
* Background workers
* Task history tracking
* Persistent task storage

### Monitoring

* Agent execution metrics
* Analytics dashboard
* Task status tracking

### Deployment

* Dockerized application
* Persistent database volumes
* Environment variable management

## Architecture

```text
Streamlit Dashboard
        │
        ▼
     FastAPI
        │
        ▼
   Task Executor
        │
 ┌──────┼──────┐
 ▼      ▼      ▼
Research Planner Summarizer
 Agent    Agent    Agent
        │
        ▼
     Groq LLM
        │
        ▼
      SQLite
```

## Technology Stack

### Backend

* Python
* FastAPI
* SQLite
* Pydantic

### Frontend

* Streamlit

### AI

* Groq API
* Multi-Agent Architecture

### Deployment

* Docker

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd AI_OS_DEV
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create `.env`

```env
GROQ_API_KEY=your_api_key_here
```

### Start Backend

```bash
uvicorn src.api.main:app --reload
```

### Start Frontend

```bash
streamlit run src/ui/app.py
```

## Docker

### Build

```bash
docker build -t devmind-ai .
```

### Run

```bash
docker run --name devmind-ai-container --env-file .env -v ${PWD}/data:/app/data -p 8000:8000 devmind-ai
```

## API Endpoints

### Create Task

```http
POST /task
```

### Task History

```http
GET /history
```

### Get Task

```http
GET /tasks/{task_id}
```

### Analytics

```http
GET /analytics
```

### Metrics

```http
GET /metrics
```

## Dashboard

The Streamlit dashboard provides:

* Task execution
* Live task status updates
* Analytics visualization
* Agent metrics chart
* Task history table

## Future Improvements

* Authentication
* Multi-user support
* Redis task queue
* Kubernetes deployment
* Additional AI agents
* Real-time WebSocket updates
