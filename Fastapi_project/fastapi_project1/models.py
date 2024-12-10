from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3  # Default to 3 retrieved contexts

class QueryResponse(BaseModel):
    generated_response: str
    retrieved_contexts: List[str]
