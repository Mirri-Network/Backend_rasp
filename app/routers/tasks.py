from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from services import tasks_sse

router = APIRouter()

@router.get("/tasks")
async def tasks():
    return StreamingResponse(tasks_sse(), media_type="text/event-stream")
