import cv2

# 배경 제거 객체
fgbg = cv2.createBackgroundSubtractorMOG2()
def motion_detect(frame):
    fgmask = fgbg.apply(frame)
    # 이진화
    _, th = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
    # 외곽선 찾기
    contours, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    motion_rects = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:
            x, y, w, h = cv2.boundingRect(contour)
            motion_rects.append((x, y, w, h))

    return motion_rects