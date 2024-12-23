from models import EmbeddingModel
from configs import DatabaseConnection
from PIL import Image
from io import BytesIO
import numpy as np
import face_recognition
import asyncio
from concurrent.futures import ThreadPoolExecutor

db = DatabaseConnection()
session = db.create_session()

# embedding과 user_id를 추가하는 함수
def add_embedding(user_id: str, embedding: str, user_name: str):
  new_embedding = EmbeddingModel(user_id=user_id, embedding=embedding, user_name=user_name)
  session.add(new_embedding)
  session.commit()
  session.refresh(new_embedding)
  return new_embedding

# user_id에 해당하는 embedding을 삭제하는 함수
def remove_embedding(user_id: str):
    # 특정 user_id와 일치하는 모든 레코드 가져오기
    embeddings = session.query(EmbeddingModel).filter(EmbeddingModel.user_id == user_id).all()
    
    if not embeddings:
        return None
    
    # 여러 레코드 삭제
    for embedding in embeddings:
        session.delete(embedding)
    
    # 변경사항 커밋
    session.commit()
    
    return embeddings
# 모든 embedding을 선택하는 함수
def select_all_embeddings():
  return session.query(EmbeddingModel).all()

def read_image_as_array(data: bytes) -> np.ndarray:
    # 바이트 데이터를 PIL 이미지로 변환
    pil_image = Image.open(BytesIO(data))
    # PIL 이미지를 NumPy 배열로 변환
    return np.array(pil_image)

def get_face_encoding(image_array: np.ndarray):
    encodings = face_recognition.face_encodings(image_array)
    if not encodings:
        raise ValueError("No face found in the image")
    return encodings[0].tolist()

executor = ThreadPoolExecutor()

async def process_embedding(content: bytes, user_id: str):
    image_array = read_image_as_array(content)
    return get_face_encoding(image_array)

async def file_to_embedding(content: bytes, user_id: str, user_name: str):
    image_array = read_image_as_array(content)
    encoding = await asyncio.get_event_loop().run_in_executor(executor, get_face_encoding, image_array)
    add_embedding(user_id, str(encoding), user_name)
    return user_id