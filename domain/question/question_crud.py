from datetime import datetime

from domain.question.question_schema import QuestionCreate, QuestionUpdate
from models import Question, User, Answer
from sqlalchemy import and_
from sqlalchemy.orm import Session

#skip: 총 질문 데이터 중에 건너뛰는 데이터의 수; 조회한 데이터의 시작위치
#limit: 가져오는 데이터의 수; 시작위치부터 가져올 데이터의 수
#21~30번째 데이터는 skip -> 20 ,limit -> 10
def select_question_list(db: Session, skip: int = 0, limit: int = 10, keyword: str = ''):
    question_list_all = db.query(Question)
    if keyword:
        search = '%%{}%%'.format(keyword)
        sub_query = db.query(Answer.question_id, Answer.content, User.username)\
            .outerjoin(User, and_(Answer.user_id == User.id)).subquery()
        question_list_all = question_list_all\
            .outerjoin(User)\
            .outerjoin(sub_query, and_(sub_query.c.question_id == Question.id))\
            .filter(Question.subject.ilike(search) |
                Question.content.ilike(search) |
                User.username.ilike(search) |
                sub_query.c.content.ilike(search) |
                sub_query.c.username.ilike(search)
                )
    total_num_questions =  question_list_all.distinct().count()
    question_list = question_list_all.order_by(Question.create_date.desc())\
        .offset(skip).limit(limit).all()
    return total_num_questions, question_list

def select_question(db: Session, question_id: int):
    question = db.get(Question, question_id)
    return question

#작동 순서 3. db:데베 세션, input_question: 사용자가 보낸 subject, content, user: 요청을 보낸 사용자 정보
def insert_question(db: Session, input_question: QuestionCreate, user: User):
    new_question = Question(subject = input_question.subject, content = input_question.content, create_date = datetime.now(), user = user)
    db.add(new_question)
    db.commit()

def update_question(db: Session, db_question: Question, question_update: QuestionUpdate):
    db_question.subject = question_update.subject
    db_question.content = question_update.content
    db_question.modify_date = datetime.now()
    db.add(db_question)
    db.commit()

def delete_question(db: Session, db_question: Question):
    db.delete(db_question)
    db.commit()

def recommend_question(db: Session, db_question: Question, db_user: User):
    db_question.recommend.append(db_user)
    db.commit()
""" 추천 중복 처리
def recommend_check(db: Session, db_question: Question, db_user: User):
    return db.query(Question).filter(Question.recommend.question_id == db_question.id and Question.recommend.user_id == db_user.id).first(
"""
