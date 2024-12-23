from picamera2 import Picamera2
import cv2
import numpy as np
from utils import face_detect, motion_detect

def camera_loop(process_frame=None):
    # Picamera2 객체 생성
    picam2 = Picamera2()
    
    # 카메라 설정 (예: 기본 해상도)
    picam2.configure(picam2.create_still_configuration())
    
    # 카메라 시작
    picam2.start()

    try:
        while True:
            # 프레임 캡처 (RGBA 형식으로 받아오므로 바로 BGR로 변환)
            frame = picam2.capture_array()
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            if process_frame:
                frame = process_frame(frame)

            # 프레임을 JPEG로 인코딩하고 반환
            ret, view = cv2.imencode('.jpg', frame)
            view = bytearray(view.tobytes())
            yield b'--PNPframe\r\nContent-Type: image/jpeg\r\n\r\n' + view + b'\r\n'

    finally:
        picam2.stop()