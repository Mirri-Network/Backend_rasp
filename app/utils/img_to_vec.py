import face_recognition
import json

# 인코딩할 이미지 파일 로드
images = ["obama.jpg", "biden.jpg", "jaehwan.jpg", "hyunho.jpg", "jiwon.jpg"]
names = ["Barack Obama", "Joe Biden", "Lee Jae Hwan", "Kim Hyun Ho", "Han Ji Won"]

# 인코딩을 저장할 딕셔너리 초기화
encoding_data = {"encodings": [], "names": []}

for image_path, name in zip(images, names):
    image = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(image)[0].tolist()  # JSON으로 저장하기 위해 리스트로 변환
    encoding_data["encodings"].append(encoding)
    encoding_data["names"].append(name)

# JSON 파일로 저장
with open("encodings.json", "w") as f:
    json.dump(encoding_data, f)
