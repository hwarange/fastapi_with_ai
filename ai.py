from fastapi  import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

print("OPENAI_API_KEY:", OPENAI_API_KEY)  # API 키가 제대로 로드되었는지 확인

app = FastAPI()

from openai import OpenAI

GPT_MODEL = "gpt-5.4-nano"

openai_client = OpenAI(api_key=OPENAI_API_KEY)


# 요청 데이터 구조 정의
class ChatReq(BaseModel):
    message: str

    model_config = {
        "json_schema_extra": {
            "examples": [{"message": "SSAFY 수료 기준에 대해서 알려줘"}]
        }
    }

@app.post("/chat", tags=["Chat"], summary="일반 채팅", description="GPT 모델에 메시지를 그대로 전달해 답변을 받습니다.")
def chat(req: ChatReq):
    res = openai_client.chat.completions.create(
        model=GPT_MODEL,
        messages=[{"role": "user", "content": req.message}]
    )
    return {"answer": res.choices[0].message.content}