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
        try:
            content = await image.read()
            logger.info(f"アップロードされた画像のサイズ: {len(content)} bytes")
            logger.info(f"アップロードされた画像の形式: {image.content_type}")
            
            is_valid = validate_image(content)
            if not is_valid:
                logger.warning("画像の検証に失敗しましたが、処理を続行します")
        except Exception as img_error:
            logger.error(f"画像の読み込み中にエラーが発生しました: {img_error}")
            raise HTTPException(status_code=400, detail="画像の読み込みに失敗しました。別の画像を試してください。")
        
        try:
            image_path = save_uploaded_image(content)
            logger.info(f"画像を保存しました: {image_path}")
            
            optimized_image_path = optimize_image(image_path)
            logger.info(f"画像を最適化しました: {optimized_image_path}")
        except Exception as process_error:
            logger.error(f"画像の処理中にエラーが発生しました: {process_error}")
            raise HTTPException(status_code=500, detail="画像の処理中にエラーが発生しました。もう一度お試しください。")
            
        try:
            logger.info(f"星検出を開始します: {optimized_image_path}")
            constellation_points = get_constellation_points(optimized_image_path)
            logger.info(f"星検出が完了しました: {len(constellation_points)}個のクラスタを検出")
            
            logger.info("星座の生成を開始します")
            constellation_image_path = draw_constellation_lines(optimized_image_path, constellation_points)
            logger.info(f"星座の生成が完了しました: {constellation_image_path}")
        except Exception as constellation_error:
            logger.error(f"星座の生成中にエラーが発生しました: {constellation_error}")
            raise HTTPException(status_code=500, detail="星座の生成中にエラーが発生しました。もう一度お試しください。")
        
        # 名前とストーリーの生成
        try:
            logger.info(f"星座名の生成を開始します: キーワード「{keyword}」")
            name = generate_constellation_name(keyword)
            logger.info(f"星座名が生成されました: {name}")
            
            logger.info("星座ストーリーの生成を開始します")
            story = generate_constellation_story(name, keyword)
            logger.info("星座ストーリーが生成されました")
        except Exception as openai_error:
            logger.error(f"OpenAI APIでのテキスト生成中にエラーが発生しました: {openai_error}")
            name = "未知の星座"
            story = "この星座の物語は古来より語り継がれてきましたが、詳細は時間の流れとともに失われてしまいました。"
            logger.info("エラー発生時のフォールバック: デフォルトの名前とストーリーを使用します")
        
        return {
            "status": "success",
            "message": "星座の生成が完了しました",
            "constellation_name": name,
            "story": story,
            "image_path": constellation_image_path
        }
    except Exception as e:
        logger.error(f"星座生成中にエラーが発生しました: {str(e)}")
        raise HTTPException(status_code=500, detail="星座の生成中にエラーが発生しました。もう一度お試しください。")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
