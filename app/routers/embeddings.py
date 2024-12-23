from fastapi import APIRouter, UploadFile, File, Form
from schemas import UserIdSchema
from services import remove_embedding, select_all_embeddings, file_to_embedding

router = APIRouter()

@router.post("/embedding/add")
async def create_file(file: UploadFile = File(...), user_id: str = Form(...), user_name: str = Form(...)):
    remove_embedding(user_id)
    content = await file.read()
    return await file_to_embedding(content, user_id, user_name)

@router.post("/embedding/remove")
async def remove_embedding_endpoint(user_id: UserIdSchema):
    return remove_embedding(user_id.user_id)

@router.get("/embeddings")
async def select_all_embeddings_endpoint():
    return select_all_embeddings()