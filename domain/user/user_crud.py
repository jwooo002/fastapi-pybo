from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy import or_

from domain.user.user_schema import UserCreateSchema
from models import User

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")
#bcrypt 알고리즘 사용하는 객체 생성

def insert_user(db: Session, input_user: UserCreateSchema):
    db_insert_user = User(
        username = input_user.username,
        password = pwd_context.hash(input_user.password1), #아마 여기가 암호화
        email = input_user.email
    )
    db.add(db_insert_user)
    db.commit()
    #참고로 나중에 로그인 시 입력한 비밀번호를 암호화하여 비교하면 돼서 복호화가 필요없다

def get_existing_user(db: Session, input_user: UserCreateSchema):
    return db.query(User).filter(
        or_(User.username == input_user.username,
            User.email == input_user.email)
    ).first()
#filter : 데이터베이스에서 특정 조건을 만족하는 레코드 필터링(찾는다)
#User가 User테이블을 말함, 이 비교는 데이터베이스 엔진이 실행하고 필요한 경우 모든 레코드 확인함
#같은 레코드가 있으면 그 레코드를 반환 User(id = 무엇, username = 무엇 ...)

def get_user(db: Session, input_username: str):
    return db.query(User).filter(User.username == input_username).first()