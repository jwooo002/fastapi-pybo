from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

from database import Base

#question_voter는 질문 추천을 위해 사용할 테이블 객체
question_recommend = Table(
    'question_recommend', #테이블 이름
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('question_id', Integer, ForeignKey('question.id'), primary_key=True)
) #사용자 id와 질문 id를 쌍으로 가짐 이 두개가 프라이머리키이므로 다대다 관계를 의미

answer_recommend = Table(
    'answer_recommend',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key = True),
    Column('answer_id', Integer, ForeignKey('answer.id'), primary_key = True)
)

#Question Model
class Question(Base): #inherit Base
    __tablename__ = "question" # means table name managed by model

    id = Column(Integer, primary_key = True)
    subject = Column(String, nullable = False) # String : 글자 수 제한된 텍스트
    content = Column(Text, nullable = False) # Text : 글자 수 제한할 수 없는 텍스트
    create_date = Column(DateTime, nullable = False) # nullable = False : can store null in attribute
    user_id = Column(Integer, ForeignKey("user.id"), nullable = True) #User모델과 Question모델 연결
    user = relationship("User", backref = "question_users")
    modify_date = Column(DateTime, nullable = True)
    recommend = relationship("User", secondary=question_recommend, backref="question_recommends")

#Answer Model
class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key = True)
    content = Column(Text, nullable = False)
    create_date = Column(DateTime, nullable = False)
    question_id = Column(Integer, ForeignKey("question.id")) # question.id means id column of Question table
    question = relationship("Question", backref = "answers")#relationship() enable question refer to answers
    user_id = Column(Integer, ForeignKey("user.id"), nullable = True)
    user = relationship("User", backref = "answer_users")
    modify_date = Column(DateTime, nullable = True)
    recommend = relationship('User', secondary = answer_recommend, backref = 'answer_recommends')

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key = True)
    username = Column(String, unique = True, nullable = False)
    password = Column(String, nullable = False)
    email = Column(String, unique = True, nullable = False)