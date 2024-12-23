from pydantic import BaseModel

class EmbeddingSchema(BaseModel):
    user_id: str
    embedding: str

class UserIdSchema(BaseModel):
    user_id: str