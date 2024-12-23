from configs import DatabaseConnection
from schemas import TaskSchema
from models import TaskModel, EmbeddingModel
import asyncio, json
from sqlalchemy.sql import text

db = DatabaseConnection()
session = db.create_session()

def create_safe_session():
    db = DatabaseConnection()
    return db.create_session()

def get_user_name_by_user_id(user_id: str):
    with create_safe_session() as session:
        query = text("SELECT user_name FROM embeddings WHERE user_id = :user_id").execution_options(no_cache=True)
        result = session.execute(query, {"user_id": user_id}).fetchone()
        return result[0] if result else None

# user_id에 따른 tasks 조회 함수 수정
def get_tasks_by_user_id(user_id: str):
    db = DatabaseConnection()
    with db.create_session() as session:  # 독립 세션 생성
        return session.query(TaskModel).filter(TaskModel.user_id == user_id).all()
    
# 데이터베이스 업데이트나 학생 ID 변경 시에만 이벤트 전송, 현재 인식된 학생의 할 일 목록만 전송
async def tasks_sse():
    last_user_id = None
    
    while True:
        from services.face import get_current_user_id
        current_user_id = get_current_user_id()
        
        # 상태나 학생이 변경되었을 때만 새로운 할 일 목록 전송
        if last_user_id != current_user_id:
            tasks = get_tasks_by_user_id(current_user_id) if current_user_id else []
            print("cuid", current_user_id)
            user_name = get_user_name_by_user_id(current_user_id)
            tasks_data = {
                "user_name": user_name,
                "tasks": [task.to_dict() for task in tasks]
            }
            print(f"Sending updated tasks: {tasks_data}")
            yield f"data: {json.dumps(tasks_data)}\n\n"
            
            last_user_id = current_user_id
            
        await asyncio.sleep(1)
