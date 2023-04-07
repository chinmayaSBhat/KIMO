from typing import List
from pydantic import BaseModel,Field

class Chapter(BaseModel):
    name: str
    text: str
    ratings:List[int] = Field(default_factory=list)
    rating:float=0

class Course(BaseModel):
    name: str
    date: int
    description: str
    domain: List[str]
    chapters: List[Chapter]