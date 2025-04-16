from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import Optional, Union
from dotenv import load_dotenv
import logging
import os
import shutil

from app.core.star_detection import get_constellation_points, detect_stars, cluster_stars, match_constellation_with_clusters
from app.core.constellation import draw_constellation_lines
from app.core.image_processing import validate_image, save_uploaded_image, optimize_image

from app.services.openai_service import generate_constellation_name, generate_constellation_story

def process_image_and_generate_constellation(image_path, keyword):
    """
    画像処理と星座生成を行う統合関数
    
    Args:
        image_path: 処理する画像のパス
        keyword: 星座生成に使用するキーワード
        
    Returns:
        星座データを含む辞書
    """
    try:
        with open(image_path, "rb") as f:
            content = f.read()
        
        is_valid = validate_image(content)
        if not is_valid:
            raise ValueError("無効な画像形式です。JPG、PNG、AVIF、HEICなどの画像形式をお試しください。")
        
        try:
            optimized_image_path = optimize_image(image_path)
            print(f"画像を最適化しました: {optimized_image_path}")
        except Exception as optimize_error:
            print(f"画像の最適化中にエラーが発生しました: {optimize_error}")
            optimized_image_path = image_path
            print(f"最適化に失敗したため、元の画像を使用します: {image_path}")
        
        print(f"星検出を開始します: {optimized_image_path}")
        constellation_points = get_constellation_points(optimized_image_path)
        print(f"星検出が完了しました: {len(constellation_points)}個のクラスタを検出")
        
        # 星のクラスタを取得
        stars = detect_stars(
            optimized_image_path, 
            use_adaptive_threshold=True, 
            use_blob_detection=True
        )
        clusters = cluster_stars(stars, max_distance=50, min_stars=3, max_stars=12)
        print(f"クラスタリングが完了しました: {len(clusters)}個のクラスタを形成")
        
        print("星座の生成を開始します")
        constellation_result = draw_constellation_lines(optimized_image_path, constellation_points)
        constellation_image_path = constellation_result["image_path"]
        constellation_data = constellation_result["constellation_data"]
        print(f"星座の生成が完了しました: {constellation_image_path}")
        
        try:
            print(f"星座名の生成を開始します: キーワード「{keyword}」")
            name = generate_constellation_name(keyword)
            print(f"星座名が生成されました: {name}")
            
            print("星座ストーリーの生成を開始します")
            story = generate_constellation_story(name, keyword)
            print("星座ストーリーが生成されました")
            
            selected_cluster_index = match_constellation_with_clusters(name, story, clusters)
            print(f"選択されたクラスタインデックス: {selected_cluster_index}")
        except Exception as openai_error:
            print(f"OpenAI APIでのテキスト生成中にエラーが発生しました: {openai_error}")
            name = "未知の星座"
            story = "この星座の物語は古来より語り継がれてきましたが、詳細は時間の流れとともに失われてしまいました。"
            selected_cluster_index = None
            print("エラー発生時のフォールバック: デフォルトの名前とストーリーを使用します")
        
        return {
            "constellation_name": name,
            "story": story,
            "image_path": constellation_image_path,
            "stars": constellation_data["stars"],
            "constellation_lines": constellation_data["lines"],
            "selected_cluster_index": selected_cluster_index
        }
    except Exception as e:
        print(f"画像処理と星座生成中にエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        return {
            "constellation_name": "エラー",
            "story": f"星座の生成中にエラーが発生しました: {str(e)}",
            "image_path": None,
            "stars": [],
            "constellation_lines": [],
            "selected_cluster_index": None
        }


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
    allow_origins=[
        "http://localhost:5173",  # フロントエンドの開発サーバー
        "https://constellation-creator-639959525777.asia-northeast1.run.app",  # Cloud Runのドメイン
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("static/images", exist_ok=True)

# 静的ファイルの設定
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets", StaticFiles(directory="static/assets"), name="assets")


class ConstellationRequest(BaseModel):
    keyword: str


@app.get("/", response_class=HTMLResponse)
async def root():
    """フロントエンドのHTMLファイルを返す"""
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return {"message": "星AI API へようこそ！"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/api/images/{image_name}")
async def get_image(image_name: str):
    """画像ファイルを取得するエンドポイント"""
    possible_paths = [
        f"temp_{image_name}",
        f"static/images/{image_name}",
        image_name if os.path.isabs(image_name) else None,
        f"/tmp/{image_name}"
    ]
    
    possible_paths = [p for p in possible_paths if p]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"画像が見つかりました: {path}")
            return FileResponse(path)
    
    print(f"画像が見つかりません: {image_name}")
    print(f"試行したパス: {possible_paths}")
    raise HTTPException(status_code=404, detail="画像が見つかりません")


@app.post("/api/generate-constellation")
async def generate_constellation(
    keyword: str = Form(...),
    image: UploadFile = File(...)
):
    try:
        print(f"受信したキーワード: {keyword}")
        print(f"受信した画像: {image.filename}")

        # 画像を一時ファイルとして保存
        content = await image.read()
        print(f"受信した画像のサイズ: {len(content)} バイト")
        print(f"画像のMIMEタイプ: {image.content_type}")
        
        is_valid = validate_image(content)
        if not is_valid:
            raise HTTPException(status_code=400, detail="無効な画像形式です。JPG、PNG、AVIF、HEICなどの画像形式をお試しください。")
        
        try:
            temp_image_path = save_uploaded_image(content, "/tmp")
            print(f"画像を保存しました: {temp_image_path}")
        except Exception as save_error:
            print(f"画像の保存中にエラーが発生しました: {save_error}")
            temp_image_path = f"/tmp/temp_{image.filename}"
            with open(temp_image_path, "wb") as buffer:
                buffer.write(content)
            print(f"フォールバック: 画像を一時ファイルに保存しました: {temp_image_path}")

        # 画像処理とコンステレーション生成
        constellation_data = process_image_and_generate_constellation(temp_image_path, keyword)
        
        print("生成された星座データ:")
        print(f"- 星座名: {constellation_data['constellation_name']}")
        print(f"- ストーリー: {constellation_data['story']}")
        print(f"- 星の数: {len(constellation_data.get('stars', []))}")
        print(f"- ラインの数: {len(constellation_data.get('constellation_lines', []))}")

        constellation_image_path = constellation_data["image_path"]
        static_image_filename = os.path.basename(constellation_image_path)
        static_image_path = f"static/images/{static_image_filename}"
        
        try:
            shutil.copy(constellation_image_path, static_image_path)
            print(f"画像を静的ディレクトリにコピーしました: {static_image_path}")
        except Exception as copy_error:
            print(f"画像のコピー中にエラーが発生しました: {copy_error}")
        
        image_url = f"/api/images/{static_image_filename}"
        
        # レスポンスを返す前に形式を確認
        response_data = {
            "constellation_name": constellation_data["constellation_name"],
            "story": constellation_data["story"],
            "image_path": image_url,
            "stars": constellation_data.get("stars", []),
            "constellation_lines": constellation_data.get("constellation_lines", []),
            "selected_cluster_index": constellation_data.get("selected_cluster_index", None)
        }

        print("APIレスポンス:", response_data)
        return response_data

    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
