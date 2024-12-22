from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.status import HTTP_400_BAD_REQUEST

from database import get_db
from domain.question import question_schema, question_crud
from domain.user.user_router import get_current_user
from models import User

router = APIRouter(
    prefix="/api/question",
)
#APIRouter는 여러 API 엔드포인트를 그룹화하거나 특정 고통 설정(URL prefix, 종속성 태그 등)을 적용하기 위한 클래스
#router는 APIRouter 클래스의 인스턴스
#prefix는 라우터에 등록된 모든 엔드포인트 경로 앞에 자동으로 추가되는 RUL 경로
#APIRouter로 생성된 객체(router)는 FASTAPI 앱에 포함되어야 한다(main.py에 있음) 객체.include_router()를 통해

#question_schema.QuestionList 클래스에 Question 리스트랑 총 데이터 수(int)가 있음 원래 list[Question]대체
@router.get("/list", response_model = question_schema.QuestionList)
#response_model은 반환값의 데이터 모델을 정의, list[question_schema.Question]는 반환값이 question_schema.Question 객체의 리스트라는 것
def get_question_list(db: Session = Depends(get_db), page: int = 0, size: int = 10, keyword: str = ''):
    total, question_list = question_crud.select_question_list(db, skip = page * size, limit = size, keyword = keyword)
    return { 'total': total, 'question_list': question_list }
#_question_list를 fastapi 엔드포인트의 반환값으로 지정한다.
#fastapi는 이 데이터를 json으로 자동 변환하여 클라이언트에 반환한다.
#list[question_schema.Question]로 지정된 모델을 기반으로 반환값을 변환(pydantic으로)
#fastapi는 변환된 json 데이터를 http응답 본문(body)에 포함시킴
#http 응답 헤더에 Content-Typ: application/json을 추가
"""
fastapi의 응답 처리 흐름
클라이언트가 /list로 요청을 보냄.
FastAPI는 요청 URL과 메서드를 보고, 해당 요청을 처리할 함수(question_list)를 찾음.
question_list 함수가 실행되고, return _question_list로 반환된 데이터가 FastAPI로 전달됨.
FastAPI는 이 데이터를:
response_model로 검증.
JSON으로 직렬화.
HTTP 응답으로 생성.
최종적으로 클라이언트에 HTTP 응답이 전송됨.
"""
"""
@router.get 데코레이터는 router.get() 메서드가 반환한 함수로 question_list를 감싸는 역할
router.get("/list") 메서드 호출:
흐름 
FastAPI가 /list 경로와 GET 요청을 처리할 준비를 함.
router.get은 내부적으로 question_list를 받아서 FastAPI 내부에 등록.
데코레이터가 적용된 함수의 동작:

클라이언트가 /list로 요청을 보내면, FastAPI가 question_list를 호출.
반환값을 JSON 응답으로 직렬화.
"""
#데코레이터 한 번에 이해: 내가 입맛대로 바꿀 함수를 작성하고 그 함수를 기본 기능을 제공하는 곳에 데코레이터로 등록한다.
#그곳에서 알아서 필요할 때 내 함수를 가져다 쓴다.

#아마도 response_model은 반환 형식을 설정하는 것 같다.
@router.get("/detail/{question_id}", response_model = question_schema.Question)
#/detail/2와 같은 URL 요청 받으면 {question_id}로 2를 받음, 그게 밑에 함수에 반환된다
def question_detail(question_id: int, db: Session = Depends(get_db)):
    question = question_crud.select_question(db, question_id = question_id)
    return question

#라우터 함수의 응답으로 response_model을 사용하는 대신status_code = status.HTTP_204_NO_CONTENT을 사용함
#이렇게 리턴할 응답이 없는 경우 204를 리턴하여 "응답 없음"을 나타낼 수 있다.
#작동 순서 1. 클라이언트에서 /create api로 post요청(json으로 subject와 content)
#2. question_create함수 호출, input_question은 QuestionCreate 스키마 사용
#4. 데이터 저장 후 204 no content 반환(성공)
@router.post("/create", status_code = status.HTTP_204_NO_CONTENT)
def question_create(
        input_question: question_schema.QuestionCreate, #여기서 question_schema로 넘어감
        db: Session = Depends(get_db), #의존성 주입, 여기서 question_create함수가 핸들러 함수, 핸들러함수가 끝나면 fianlly가 실행
        current_user: User = Depends(get_current_user) #의존성 주입
):
    #insert_question 함수 호출
    question_crud.insert_question(db=db, input_question=input_question, user=current_user)

#Depends 설명
#get_db → yield로 db 반환(핸들러 함수 실행 동안 유지 → 핸들러 실행 → 핸들러 종료 → get_db의 finally에서 db.close() 실행.
#depends는 제너레이터 함수를 실행하고 종료하는 듯, 맨 처음과 마지막에 depends가 있는 것
#요청 → Depends(get_db) 호출 → get_db 실행 → db 반환(yield)→ 핸들러 함수 실행(db 사용) → 핸들러 종료 → finally 실행(db.close())→ get_db 종료
@router.put("/update", status_code = status.HTTP_204_NO_CONTENT)
def question_update(input_question: question_schema.QuestionUpdate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)
):
    #원래 question 레코드 객체화
    db_question = question_crud.select_question(db, question_id = input_question.question_id)
    if not db_question: #db_question is False
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "No data found")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Unauthorized modification")
    question_crud.update_question(db = db, db_question = db_question, question_update = input_question)

@router.delete("/delete", status_code = status.HTTP_204_NO_CONTENT)
def question_delete(delete_question: question_schema.QuestionDelete,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)
):
    db_question = question_crud.select_question(db, question_id = delete_question.question_id)
    if not db_question:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "No data found")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Unauthorized delete")
    question_crud.delete_question(db = db, db_question = db_question)

@router.post("/recommend", status_code = status.HTTP_204_NO_CONTENT)
def question_recommend(recommend_question: question_schema.QuestionRecommend,
                       db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)
):
    db_question = question_crud.select_question(db, question_id = recommend_question.question_id)
    if not db_question:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "No data found")
    question_crud.recommend_question(db, db_question = db_question, db_user = current_user)