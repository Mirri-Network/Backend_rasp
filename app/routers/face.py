from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from services import face_detect_sse

router = APIRouter()

@router.get("/face/detect", tags=["face"])
async def face_detect():
    return StreamingResponse(face_detect_sse(), media_type="text/event-stream")

@router.post("/face/add", tags=["face"])
async def face_add():
    return {"message": "Face added"}