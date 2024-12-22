from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo
#EmailStr: 이메일 형식과 일치하는지 검증

class UserCreateSchema(BaseModel):
    username: str
    password1: str
    password2: str
    email: EmailStr

    #4개의 필드(클래스에 있는 변수 말하는 듯)가 빈 값이 아니게
    @field_validator('username', 'password1', 'password2', 'email')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('not accept empty value')
        return v

    #password1, password2가 동일한지 검증
    @field_validator('password2')
    def password_match(cls, v, info: FieldValidationInfo):
        if 'password1' in info.data and v != info.data['password1']:
            #info.data에 UserCreate의 속성들이 {변수명:값, ...} 형태로 전달된다.
            raise ValueError('not match password')
        return v

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str

class User(BaseModel):
    id: int
    username: str
    email: str