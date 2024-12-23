from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from services import weather_sse

router = APIRouter()

@router.get("/weather")
async def weather():
    return StreamingResponse(weather_sse(), media_type="text/event-stream")