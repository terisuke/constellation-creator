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
        image = Image.open(io.BytesIO(file_content))
        image.verify()  # 画像が有効かどうかを検証
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
        os.makedirs(output_dir, exist_ok=True)
        
        import uuid
        filename = f"{uuid.uuid4()}.jpg"
        output_path = os.path.join(output_dir, filename)
        
        image = Image.open(io.BytesIO(file_content))
        image.save(output_path)
        
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
        image = Image.open(image_path)
        
        image = image.resize(target_size, Image.Resampling.LANCZOS)
        
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image = cv2.equalizeHist(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        
        output_path = image_path.rsplit(".", 1)[0] + "_optimized." + image_path.rsplit(".", 1)[1]
        
        cv2.imwrite(output_path, image)
        
        logger.info(f"画像を最適化しました: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"画像の最適化中にエラーが発生しました: {e}")
        raise
