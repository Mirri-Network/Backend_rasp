import asyncio
import time
import cv2
from utils import face_detect
from threading import Thread
from picamera2 import Picamera2

# 전역 상태 변수들
face_detected = False  # 현재 얼굴 감지 상태
is_thread_started = False  # 감지 스레드 실행 상태
current_user_id = None  # 현재 인식된 학생 ID

# 현재 인식된 학생 ID를 반환하는 함수
def get_current_user_id():
    return current_user_id

# 얼굴 감지 스레드를 시작하는 함수. 한 번만 실행되도록 보장
def start_detection_thread():
    global is_thread_started
    if not is_thread_started:
        Thread(target=detect_face_loop, daemon=True).start()
        is_thread_started = True

# 카메라로 얼굴을 지속적으로 감지하는 메인 루프
def detect_face_loop():
    global face_detected, current_user_id
    picam2 = Picamera2()
    
    # 카메라 설정 (예: 기본 해상도)
    picam2.configure(picam2.create_still_configuration())
    
    # 카메라 시작
    picam2.start()

    try:
        while True:
            frame = picam2.capture_array()
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # 얼굴 감지 수행
            _, face_names = face_detect(frame)
            print(face_names)
            new_status = bool(face_names)
            # Unknown이 아닌 경우에만 학생 ID로 인정, 감지된 얼굴이 있으면 학생 ID를 추출
            new_user_id = face_names[0] if face_names and face_names[0] != 'Unknown' else None

            # 상태나 학생 ID가 변경될 경우 업데이트
            if new_status != face_detected or new_user_id != current_user_id:
                print(f"Status changed: {new_status}, Student ID: {new_user_id}")
                # 상태 변경시 전역 변수 업데이트
                face_detected = new_status
                current_user_id = new_user_id

            time.sleep(0.1)
    finally:
        picam2.stop()

async def face_detect_sse():
    start_detection_thread()
    previous_status = face_detected

    while True:
        # 상태가 변경되었을 때만 이벤트 전송
        if previous_status != face_detected:
            yield f"data: {str(face_detected).lower()}\n\n"
            previous_status = face_detected
            print(f"Sending updated status: {face_detected}")
        await asyncio.sleep(0.1)
