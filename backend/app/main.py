from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Union
from dotenv import load_dotenv
import logging
import os

from app.core.star_detection import get_constellation_points
from app.core.constellation import draw_constellation_lines
from app.core.image_processing import validate_image, save_uploaded_image, optimize_image

from app.services.openai_service import generate_constellation_name, generate_constellation_story


# 環境変数の読み込み
load_dotenv()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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


@app.get("/")
async def root():
    return {"message": "星AI API へようこそ！"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/api/generate-constellation")
async def generate_constellation(
    keyword: str = Form(...),
    image: UploadFile = File(...)
):
    try:
        print(f"受信したキーワード: {keyword}")
        print(f"受信した画像: {image.filename}")

        # 画像を一時ファイルとして保存
        temp_image_path = f"temp_{image.filename}"
        with open(temp_image_path, "wb") as buffer:
            content = await image.read()
            buffer.write(content)

        # 画像処理とコンステレーション生成
        constellation_data = process_image_and_generate_constellation(temp_image_path, keyword)
        
        print("生成された星座データ:")
        print(f"- 星座名: {constellation_data['constellation_name']}")
        print(f"- ストーリー: {constellation_data['story']}")
        print(f"- 星の数: {len(constellation_data.get('stars', []))}")
        print(f"- ラインの数: {len(constellation_data.get('constellation_lines', []))}")

        # レスポンスを返す前に形式を確認
        response_data = {
            "constellation_name": constellation_data["constellation_name"],
            "story": constellation_data["story"],
            "image_path": temp_image_path,
            "stars": constellation_data.get("stars", []),
            "constellation_lines": constellation_data.get("constellation_lines", [])
        }

        print("APIレスポンス:", response_data)
        return response_data

    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
