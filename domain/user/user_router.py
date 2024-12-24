from datetime import datetime, timedelta, timezone
from logging import getLogger

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status
from starlette.config import Config

from database import get_db
from domain.user import user_crud, user_schema
from domain.user.user_crud import pwd_context

logger = getLogger(__name__)
config = Config('.env')

ACCESS_TOKEN_EXPIRE_MINUTES = int(config('ACCESS_TOKEN_EXPIRE_MINUTES')) #토큰의 유효기간 (분 단위)
SECRET_KEY = config('SECRET_KEY') #암호화 시 사용하는 64자리 랜덤 문자열
ALGORITHM = "HS256" #토큰 생성 시 사용하는 알고리즘
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/api/user/login") #토큰url은 로그인 api의 url의미

router = APIRouter(
    prefix = "/api/user",
)

@router.post("/create", status_code = status.HTTP_204_NO_CONTENT)
def user_create(input_user: user_schema.UserCreateSchema, db: Session = Depends(get_db)):
    is_existing_user = user_crud.get_existing_user(db, input_user = input_user)
    if is_existing_user:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "already existing user")
    user_crud.insert_user(db = db, input_user = input_user)

@router.post("/login", response_model = user_schema.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #login api의 입력항목인 username과 password 값은 OAuth뭐시기를 통해 얻어옴튕기다
    #check user and password
    user = user_crud.get_user(db, form_data.username)
    #username으로 사용자 모델 객체를 가져옴
    #form_data가 입력한 데이터일 듯 그거랑 데베에 있는 거랑 비교
    #verify 함수는 암호화되지 않은 비밀번호를 암호화 해서 데베에 저장된 암호와 일치하는지 판단
    #조건에 해당하는 사용자를 못찾거나 비밀번호가 일치하지 않으면 401오류(사용자 인증 오류) 리턴
    if not user or not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect username or password",
            headers = {"WWW-Authenticate": "Bearer"},
        )

    #make access token
    #sub 항목 : 사용자 이름, exp 항목 : 토큰의 유효기간 => 토큰 생성
    data = {
        "sub": user.username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm = ALGORITHM)
    #토큰 암호화 해서 저장(암호화에 사용되는 비밀 키와 암호화 알고리즘)

    return { "access_token" : access_token, "token_type" : "bearer", "username" : user.username }
    #username이 암호화되지 않은 것은 토큰은 인증과 인가 과정에서 사용되고 유저 이름은 프론트 UI에 표시하거나 다른 거에 필요할 수 있음

#매개변수로 사용한 토큰 값은 OAuth2PasswordBearer에 의해 자동 매핑
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    no_username_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials - no username",
        headers = {"WWW-Authenticate": "Bearer"},
    )
    jwt_error_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials - jwt error",
        headers={"WWW-Authenticate": "Bearer"},
    )
    no_user_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials - does not exist user",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM]) #토큰 복호화, 사용자명 get
        username: str = payload.get("sub")
        #exp_time: datetime.date = payload.get("exp") !!expire time exception
        #logger.debug(f"exp_time : {exp_time}")
        if username is None:
            raise no_username_exception
    except JWTError:
        raise jwt_error_exception
    else:
        user = user_crud.get_user(db, input_username = username)
        if user is None:
            raise no_user_exception
        return user #사용자 객체 리턴