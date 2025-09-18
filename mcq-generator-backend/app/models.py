# Database models for MCQ Generator
# app/models.py
from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    username: str
    password: str

class Book(BaseModel):
    id: str
    title: str
    content: str

class Question(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    book_id: str


