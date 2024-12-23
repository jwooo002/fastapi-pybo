#AWS sbmax002+241223@gamil.com

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
