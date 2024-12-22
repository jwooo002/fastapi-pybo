import datetime

from typing import List, Annotated
from pydantic import BaseModel, Field, field_validator

from domain.answer.answer_schema import Answer
from domain.user.user_schema import User

class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    answers: Annotated[List[Answer], Field(default_factory=list)] #빈 리스트 만들려면 이렇게
    user: User | None #user항목이 Question모델을 Question 스키마에 매핑할 때 자동으로 채워진다 어떻게?
    modify_date: datetime.datetime | None = None
    recommend: Annotated[List[User], Field(default_factory=list)]

class QuestionCreate(BaseModel):
    subject: str
    content: str

    # 작동 순서 2. 아래 데코레이터를 이용해서 subject와 content가 빈 값인지 확인, 빈 값이면 ValueError
    @field_validator('subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('empty value unaccepted')
        return v #유효하면 반환

class QuestionList(BaseModel):
    total: int = 0
    question_list: Annotated[List[Question], Field(default_factory = list)]

class QuestionUpdate(QuestionCreate):
    question_id: int

class QuestionDelete(BaseModel):
    question_id: int

class QuestionRecommend(BaseModel):
    question_id: int