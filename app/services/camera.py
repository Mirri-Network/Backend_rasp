import cv2
from utils import face_detect, motion_detect, camera_loop

from threading import Thread

class MyThread(Thread):
    def __init__(self, target=None, args=(), kwargs=None):
        if kwargs is None:
            kwargs = {}
        super().__init__(target=target, args=args, kwargs=kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def get_result(self):
        return self._return


def camera_detect():
    def process_frame(frame):

        # 얼굴 인식 스레드
        thread_face = MyThread(target=face_detect, args=(frame,))
        thread_face.start()

        thread_face.join()
        # 스레드가 완료 대기 및 결과 저장
        face_locations, face_names = thread_face.get_result()

        # 감지된 얼굴에 사각형과 이름 추가
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)  # 빨간색 박스
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        return frame

    # 카메라 루프 시작
    return camera_loop(process_frame)