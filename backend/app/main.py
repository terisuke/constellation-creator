from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv


# 環境変数の読み込み
load_dotenv()


app = FastAPI(
    title="星AI API",
    description='AIがあなたの"今夜だけの星座"を作るAPI',
    version="0.1.0"
)


# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # フロントエンドの開発サーバー
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConstellationRequest(BaseModel):
    keyword: str
    generate_image: bool = False


@app.get("/")
async def root():
    return {"message": "星AI API へようこそ！"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/api/generate-constellation")
async def generate_constellation(
    request: ConstellationRequest,
    image: Optional[UploadFile] = File(None)
):
    try:
        # TODO: 1. 画像の処理（アップロードまたは生成）
        # TODO: 2. 星の検出
        # TODO: 3. 星座の生成
        # TODO: 4. 名前とストーリーの生成
        return {
            "status": "success",
            "message": "星座の生成が完了しました",
            "constellation_name": "サンプル星座",
            "story": "これはサンプルのストーリーです。"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
