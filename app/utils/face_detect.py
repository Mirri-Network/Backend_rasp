import face_recognition, cv2, numpy as np, json, os, time, threading
from models import EmbeddingModel
from configs import DatabaseConnection
from sqlalchemy.sql import text

# 등록된 얼굴 임베딩
# 등록된 얼굴 임베딩을 저장할 변수
known_face_encodings = []
known_face_names = []

# 데이터베이스에서 인코딩 데이터를 불러오는 함수
def load_encodings_from_db():
    global known_face_encodings, known_face_names
    db = DatabaseConnection()
    session = db.create_session()
    try:
        # SQL 쿼리를 명시적으로 작성하며 캐싱 비활성화
        query = text("SELECT embedding, user_id FROM embeddings").execution_options(no_cache=True)
        result = session.execute(query).fetchall()

        # 결과 처리
        known_face_encodings = [np.array(json.loads(row[0])) for row in result]
        known_face_names = [row[1] for row in result]

        print(known_face_names, "로딩 성공")
    finally:
        session.close()


# 10초마다 인코딩 데이터를 불러오는 폴링 함수
def polling_encodings():
    while True:
        load_encodings_from_db()
        time.sleep(10)

# 폴링 스레드 시작
polling_thread = threading.Thread(target=polling_encodings, daemon=True)
polling_thread.start()

def face_detect(frame):
    # 프레임 크기 축소, BGR to RGB, to NumpyArray
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    rgb_small_frame_np = np.array(rgb_small_frame)

    # 얼굴 위치와 인코딩 찾기
    face_locations = face_recognition.face_locations(rgb_small_frame_np)
    face_encodings = face_recognition.face_encodings(rgb_small_frame_np, face_locations)

    # 얼굴 이름 저장할 리스트
    face_names = []
               
    for face_encoding in face_encodings:
        # 알려진 얼굴과 비교
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.43)
        name = "Unknown"

        # 가장 가까운 얼굴을 찾기
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
        face_names.append(name)

    # 얼굴 위치를 원래 크기로 변환
    face_locations = [(top*4, right*4, bottom*4, left*4) for (top, right, bottom, left) in face_locations]

    return face_locations, face_names