from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from domain.question import question_router
from domain.answer import answer_router
from domain.user import user_router

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, #Allow Svelte develop server address
    allow_credentials=True,
    allow_methods=["*"], #Allow all http method(GET, POST etc...)
    allow_headers=["*"], #Allow all header
)

app.include_router(question_router.router)
app.include_router(answer_router.router)
app.include_router(user_router.router)
app.mount("/assets", StaticFiles(directory = "frontend/dist/assets")) #frontend/dist/assets디렉터리를 /assets(index.html 파일 안에) 경로로 매핑할 수 있게 함

# "/" 경로로 접속하면 index.html 파일을 읽어서 서비스 할 수 있도록 하는 함수
@app.get("/")
def index():
    return FileResponse("frontend/dist/index.html")

"""
@app.get('/')
def default():
    return 'fuck'

@app.get("/hello") #데코레이터. /hello라는 URL요청이 발생하면 해당 함수를 실행하여 결과를 리턴하라.
def hello():
    return {"message" : "hi pybo"}
"""

"""
# 샘플 Python 스크립트입니다.

# Ctrl+F5을(를) 눌러 실행하거나 내 코드로 바꿉니다.
# 클래스, 파일, 도구 창, 액션 및 설정을 어디서나 검색하려면 Shift 두 번을(를) 누릅니다.


def print_hi(name):
    # 스크립트를 디버그하려면 하단 코드 줄의 중단점을 사용합니다.
    print(f'Hi, {name}')  # 중단점을 전환하려면 F9을(를) 누릅니다.


# 스크립트를 실행하려면 여백의 녹색 버튼을 누릅니다.
if __name__ == '__main__':
    print_hi('PyCharm')

# https://www.jetbrains.com/help/pycharm/에서 PyCharm 도움말 참조
"""