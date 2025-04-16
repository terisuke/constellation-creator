import os
import sys
import logging
from PIL import Image
import io
import cv2
import numpy as np
import subprocess
import tempfile

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.image_processing import validate_image, save_uploaded_image, optimize_image
from app.core.star_detection import detect_stars, load_image
from app.core.constellation import draw_constellation_lines

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def convert_to_avif(input_path, output_path=None):
    """
    JPG画像をAVIF形式に変換する
    
    Args:
        input_path: 入力画像のパス
        output_path: 出力画像のパス（指定がない場合は自動生成）
        
    Returns:
        変換された画像のパス
    """
    if output_path is None:
        output_path = input_path.rsplit(".", 1)[0] + ".avif"
    
    try:
        convert_cmd = ['convert', input_path, output_path]
        result = subprocess.run(convert_cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(output_path):
            logger.info(f"画像をAVIF形式に変換しました: {output_path}")
            return output_path
        else:
            logger.error(f"AVIF変換に失敗しました: {result.stderr}")
            return None
    except Exception as e:
        logger.error(f"AVIF変換中にエラーが発生しました: {e}")
        return None

def test_avif_support():
    """AVIFフォーマットのサポートをテストする"""
    try:
        sample_path = "../frontend/public/sample.jpg"
        
        if not os.path.exists(sample_path):
            logger.error(f"サンプル画像が見つかりません: {sample_path}")
            return False
        
        temp_dir = tempfile.mkdtemp()
        avif_path = os.path.join(temp_dir, "sample.avif")
        
        logger.info(f"サンプル画像をAVIF形式に変換します: {sample_path} -> {avif_path}")
        convert_cmd = ['convert', sample_path, avif_path]
        result = subprocess.run(convert_cmd, capture_output=True, text=True)
        
        if result.returncode != 0 or not os.path.exists(avif_path):
            logger.error(f"AVIF変換に失敗しました: {result.stderr}")
            return False
        
        logger.info(f"AVIF画像のサイズ: {os.path.getsize(avif_path)} bytes")
        
        logger.info("load_image関数でAVIF画像を読み込みます")
        image = load_image(avif_path)
        if image is None:
            logger.error("AVIF画像の読み込みに失敗しました")
            return False
        
        logger.info(f"AVIF画像を正常に読み込みました: {image.shape}")
        
        with open(avif_path, 'rb') as f:
            avif_data = f.read()
        
        logger.info("validate_image関数でAVIFバイナリデータを検証します")
        is_valid = validate_image(avif_data)
        logger.info(f"AVIF画像の検証結果: {is_valid}")
        
        logger.info("save_uploaded_image関数でAVIFバイナリデータを保存します")
        saved_path = save_uploaded_image(avif_data)
        if not os.path.exists(saved_path):
            logger.error(f"AVIF画像の保存に失敗しました")
            return False
        
        logger.info(f"AVIF画像を正常に保存しました: {saved_path}")
        
        logger.info("optimize_image関数でAVIF画像を最適化します")
        optimized_path = optimize_image(saved_path)
        if not os.path.exists(optimized_path):
            logger.error(f"AVIF画像の最適化に失敗しました")
            return False
        
        logger.info(f"AVIF画像を正常に最適化しました: {optimized_path}")
        
        logger.info("detect_stars関数でAVIF画像から星を検出します")
        stars = detect_stars(optimized_path)
        logger.info(f"AVIF画像から{len(stars)}個の星を検出しました")
        
        try:
            os.remove(avif_path)
            os.remove(saved_path)
            os.remove(optimized_path)
            os.rmdir(temp_dir)
        except:
            pass
        
        return True
    except Exception as e:
        logger.error(f"AVIFサポートテスト中にエラーが発生しました: {e}")
        return False

if __name__ == "__main__":
    success = test_avif_support()
    if success:
        logger.info("AVIFサポートテストが成功しました！")
        sys.exit(0)
    else:
        logger.error("AVIFサポートテストが失敗しました")
        sys.exit(1)
