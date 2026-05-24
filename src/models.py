from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Task(BaseModel):

    id: str

    user_input: str

    agent: Optional[str] = None

    status: str = "pending"

    result: Optional[str] = None

    created_at: datetime = datetime.now()