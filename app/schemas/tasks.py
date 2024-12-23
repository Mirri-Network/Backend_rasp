from pydantic import BaseModel

class TaskSchema(BaseModel):
    task: str
    user_id: str
    
class TaskDelete(BaseModel):
    task_id: int