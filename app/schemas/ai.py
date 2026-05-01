from pydantic import BaseModel

class AIQuestion(BaseModel):
    question: str

class AIAnswer(BaseModel):
    answer: str