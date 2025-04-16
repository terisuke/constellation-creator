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
from app.services.stable_diffusion import generate_starry_image


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
    generate_image: bool = False


@app.get("/")
async def root():
    return {"message": "星AI API へようこそ！"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/api/generate-constellation")
async def generate_constellation(
    keyword: str = Form(...),
    generate_image: str = Form('false'),
    image: Optional[UploadFile] = File(None)
):
    try:
        # 画像処理（アップロードまたは生成）
        if image:
            content = await image.read()
            if not validate_image(content):
                raise HTTPException(status_code=400, detail="無効な画像形式です")
            image_path = save_uploaded_image(content)
            optimized_image_path = optimize_image(image_path)
        elif generate_image.lower() == 'true':
            image_path = generate_starry_image(keyword)
            optimized_image_path = image_path
        else:
            raise HTTPException(status_code=400, detail="画像が提供されていません")
            
        constellation_points = get_constellation_points(optimized_image_path)
        
        constellation_image_path = draw_constellation_lines(optimized_image_path, constellation_points)
        
        # 名前とストーリーの生成
        name = generate_constellation_name(keyword)
        story = generate_constellation_story(name, keyword)
        
        return {
            "status": "success",
            "message": "星座の生成が完了しました",
            "constellation_name": name,
            "story": story,
            "image_path": constellation_image_path
        }
    except Exception as e:
        logger.error(f"星座生成中にエラーが発生しました: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
