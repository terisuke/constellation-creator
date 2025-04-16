import cv2
import numpy as np
from PIL import Image
import os
import logging
from typing import Tuple, Optional
import io

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_image(file_content: bytes) -> bool:
    """
    アップロードされた画像が有効かどうかを検証する
    
    Args:
        file_content: 画像ファイルのバイト内容
        
    Returns:
        有効な場合はTrue、そうでない場合はFalse
    """
    try:
        # 画像データが空でないことを確認
        if not file_content:
            logger.error("画像データが空です")
            return False
            
        # 画像を開いて検証
        image = Image.open(io.BytesIO(file_content))
        image.verify()  # 画像が有効かどうかを検証
        
        # 画像サイズの確認
        width, height = image.size
        if width == 0 or height == 0:
            logger.error("画像サイズが無効です")
            return False
            
        return True
    except Exception as e:
        logger.error(f"無効な画像ファイル: {e}")
        return False

def save_uploaded_image(file_content: bytes, output_dir: str = "/tmp") -> str:
    """
    アップロードされた画像を一時ファイルとして保存する
    
    Args:
        file_content: 画像ファイルのバイト内容
        output_dir: 出力ディレクトリ
        
    Returns:
        保存された画像のパス
    """
    try:
        # 出力ディレクトリの作成
        os.makedirs(output_dir, exist_ok=True)
        
        # ファイル名の生成
        import uuid
        filename = f"{uuid.uuid4()}.jpg"
        output_path = os.path.join(output_dir, filename)
        
        # 画像の保存
        image = Image.open(io.BytesIO(file_content))
        # RGBモードに変換（透過画像の場合に対応）
        if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
            image = image.convert('RGB')
        image.save(output_path, 'JPEG', quality=95)
        
        logger.info(f"アップロードされた画像を保存しました: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"画像の保存中にエラーが発生しました: {e}")
        raise

def optimize_image(image_path: str, target_size: Tuple[int, int] = (800, 600)) -> str:
    """
    画像を最適化する（リサイズ、コントラスト調整など）
    
    Args:
        image_path: 処理する画像のパス
        target_size: 目標サイズ（幅, 高さ）
        
    Returns:
        最適化された画像のパス
    """
    try:
        # 画像の読み込み
        image = Image.open(image_path)
        
        # RGBモードに変換
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # アスペクト比を保持してリサイズ
        image.thumbnail(target_size, Image.Resampling.LANCZOS)
        
        # NumPy配列に変換
        image_array = np.array(image)
        
        # OpenCV形式に変換
        image_cv = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
        
        # グレースケール変換
        gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
        
        # コントラスト調整
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        # BGRに戻す
        enhanced_bgr = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)
        
        # 出力パスの生成
        output_path = image_path.rsplit(".", 1)[0] + "_optimized." + image_path.rsplit(".", 1)[1]
        
        # 画像の保存
        cv2.imwrite(output_path, enhanced_bgr)
        
        logger.info(f"画像を最適化しました: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"画像の最適化中にエラーが発生しました: {e}")
        raise
