from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.config import Config

config = Config('.env')
SQLALCHEMY_DATABASE_URL = config('SQLALCHEMY_DATABASE_RUL') #Config 클래스 이용, .env파일의 변수 읽기 가능
"""
SQLALCHEMY_DATABASE_URL : Database access address
sqlite:///./myapi.db : mean sqlite3 database file and save project root directory 
"""

engine = create_engine( #create connection pool; connection pool limit number of instance that access database
    SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread" : False}
)
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
"""
    SessionLocal is class need for using access database
    autocommit = false means 데이터 변경 시 commit 해야만 실제 저장 그리고 데이터를 잘못 저장할 경우 rollback 가능 / True일 경우 반대
    
"""
Base = declarative_base()

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
Base.metadata = MetaData(naming_convention = naming_convention)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()