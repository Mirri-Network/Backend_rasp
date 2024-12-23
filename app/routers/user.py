from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

os.environ.clear()
load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

router = APIRouter()

class OAuthCodeRequest(BaseModel):
    code: str  # 프론트엔드에서 받은 인증 코드

@router.post("/oauth/token")
async def get_oauth_token(request: OAuthCodeRequest):
    # 인증 코드로 액세스 토큰을 요청
    token_url = "https://api-auth.bssm.app/api/oauth/token"
    data = {
        "clientId": client_id,
        "clientSecret": client_secret,
        "authCode": request.code,
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=400, detail="Token request failed")
        

@router.get("/user")
async def get_user_info(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=400, detail="Authorization header missing")
    token = auth_header.split(" ")[1]
    # 액세스 토큰으로 사용자 정보를 요청
    user_info_url = "https://api-auth.bssm.app/api/oauth/resource"
    data = {
        "clientId": client_id,
        "clientSecret": client_secret,
        "token": token,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(user_info_url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=400, detail="User info request failed")