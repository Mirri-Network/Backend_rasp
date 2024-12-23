from sqlalchemy import Column, INT, VARCHAR, TEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(INT, nullable=False, autoincrement=True, primary_key=True)
    task = Column(TEXT, nullable=False)
    user_id = Column(VARCHAR, nullable=False)

    def to_dict(self):
        """객체를 사전(dict) 형태로 변환"""
        return {
            "id": self.id, 
            "task": self.task,
            "user_id": self.user_id
        }