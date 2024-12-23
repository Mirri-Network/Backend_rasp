from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from services import camera_detect

router = APIRouter()

# 얼굴, 움직임 감지
@router.get("/camera")
def camera_with_face_motion_detect():
    return StreamingResponse(camera_detect(), media_type="multipart/x-mixed-replace; boundary=PNPframe")