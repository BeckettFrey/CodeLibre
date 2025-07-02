# File: src/codelibre/graph/state.py
from pydantic import BaseModel, Field
from typing import List
from langchain_core.messages import BaseMessage


class ChatState(BaseModel):
    messages: List[BaseMessage] = Field(default_factory=list)
    system_prompt: str = ""
    response: str = ""
    reiterate: bool = False
    
    class Config:
        arbitrary_types_allowed = True  # Needed for BaseMessage