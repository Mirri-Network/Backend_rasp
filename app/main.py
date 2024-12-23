from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from routers import camera, weather, tasks, face, embeddings, user
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처에 대해 요청을 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드를 허용
    allow_headers=["*"],  # 모든 헤더를 허용
)

app.include_router(camera.router)
app.include_router(face.router)
app.include_router(weather.router)
app.include_router(tasks.router)
app.include_router(embeddings.router)
app.include_router(user.router)

templates_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../templates"))
templates = Jinja2Templates(directory=templates_dir)

@app.get("/mirror", response_class=HTMLResponse)
async def mirror_feed(request: Request): # request는 url이 아닌 모든 요청 정보를 담고있음
    return templates.TemplateResponse("index.html", {"request":request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0" ,port=8000)
