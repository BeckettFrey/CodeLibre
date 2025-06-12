from typing import Any
from pydantic import BaseModel, Field

class ChatState(BaseModel):
    """State for the chat system."""
    current_message: str = Field(default="")
    response: str = Field(default="")
    knowledge_base: Any = Field(default=None)  
