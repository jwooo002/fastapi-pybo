import datetime
from typing import Annotated, List

from pydantic import BaseModel, field_validator, Field

from domain.user.user_schema import User

class AnswerCreate(BaseModel):
    content: str #모델이 정의된 클래스 안에서 데이터를 저장하거나 다루기 위해 선언된 속성이 필드다. content는 필드다

    @field_validator('content') #필드 이름을 문자열로 받아야 함
    #목적: content 필드에 대해 값을 유효성 검사하는 메서드를 지정
    #동작: 데코레이터 아래 정의된 메서드는 content 값이 설정될 때 호출됨
    def not_empty(cls, v):
        #cls : 메서드가 클래스 메서드임을 나타냄, AnswerCreate 클래스를 참조; 그냥 이 메서드가 포함된 클래스 자체를 나타내는 듯
        #v : 필드(content)의 값
        if not v or not v.strip(): #v.strip() 문자열 앞뒤의 공백 제거, 공백만 포함된 문자열이면 빈 문자열
            raise ValueError('empty value unaccepted')
        return v
    # 이 메서드는 값을 받아 검증 후 유효하면 해당 값 반환, 그렇지 않으면 예외 발생

class Answer(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime
    user: User | None #| 는 또는 이라는 뜻인 듯
    question_id: int
    modify_date: datetime.datetime | None = None
    recommend: Annotated[List[User], Field(default_factory=list)]

class AnswerUpdate(AnswerCreate):
    answer_id: int

class AnswerDelete(BaseModel):
    answer_id: int

class AnswerRecommend(BaseModel):
    answer_id: int