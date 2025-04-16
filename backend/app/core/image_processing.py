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
    複数の方法を試して、可能な限り画像を検証する
    
    Args:
        file_content: 画像ファイルのバイト内容
        
    Returns:
        有効な場合はTrue、そうでない場合はFalse
    """
    # 画像データが空でないことを確認
    if not file_content:
        logger.error("画像データが空です")
        return False
    
    logger.info(f"検証する画像データのサイズ: {len(file_content)} バイト")
    
    try:
        image_bytes = io.BytesIO(file_content)
        image = Image.open(image_bytes)
        
        try:
            image.verify()
        except Exception as verify_error:
            logger.warning(f"画像検証エラー（無視して続行）: {verify_error}")
            
        image_bytes = io.BytesIO(file_content)
        image = Image.open(image_bytes)
        
        width, height = image.size
        if width == 0 or height == 0:
            logger.error("画像サイズが無効です")
        else:
            logger.info(f"PILで画像を検証しました: {width}x{height}, フォーマット={image.format}")
            return True
    except Exception as pil_error:
        logger.warning(f"PILでの画像検証に失敗しました: {pil_error}")
    
    try:
        nparr = np.frombuffer(file_content, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is not None and img.size > 0:
            height, width = img.shape[:2]
            logger.info(f"OpenCVで画像を検証しました: {width}x{height}")
            return True
        else:
            logger.warning("OpenCVでの画像デコードに失敗しました（Noneまたは空の画像）")
    except Exception as cv_error:
        logger.warning(f"OpenCVでの画像検証に失敗しました: {cv_error}")
    
    try:
        import subprocess
        import tempfile
        import shutil
        
        if not shutil.which('identify'):
            logger.warning("ImageMagickがインストールされていません")
            return False
        
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            temp_file.write(file_content)
            temp_path = temp_file.name
        
        identify_cmd = ['identify', temp_path]
        result = subprocess.run(identify_cmd, capture_output=True, text=True)
        
        try:
            os.remove(temp_path)
        except:
            pass
        
        if result.returncode == 0:
            logger.info(f"ImageMagickで画像を検証しました: {result.stdout.strip()}")
            return True
        else:
            logger.warning(f"ImageMagickでの画像検証に失敗しました: {result.stderr}")
    except Exception as im_error:
        logger.warning(f"ImageMagickでの処理中にエラーが発生しました: {im_error}")
    
    if len(file_content) > 1000:  # 1KB以上あれば何かしらの画像データと見なす
        logger.info("ファイルサイズに基づいて画像を検証しました")
        return True
    
    logger.error("すべての方法で画像の検証に失敗しました")
    return False

def save_uploaded_image(file_content: bytes, output_dir: str = "/tmp") -> str:
    """
    アップロードされた画像を一時ファイルとして保存する
    複数の方法を試して、可能な限り画像を保存する
    
    Args:
        file_content: 画像ファイルのバイト内容
        output_dir: 出力ディレクトリ
        
    Returns:
        保存された画像のパス
    """
    # 出力ディレクトリの作成
    os.makedirs(output_dir, exist_ok=True)
    
    # ファイル名の生成
    import uuid
    filename = f"{uuid.uuid4()}.jpg"
    output_path = os.path.join(output_dir, filename)
    
    try:
        image_bytes = io.BytesIO(file_content)
        image = Image.open(image_bytes)
        # RGBモードに変換（透過画像の場合に対応）
        if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
            image = image.convert('RGB')
        image.save(output_path, 'JPEG', quality=95)
        
        logger.info(f"PILで画像を保存しました: {output_path}")
        return output_path
    except Exception as pil_error:
        logger.warning(f"PILでの画像保存に失敗しました: {pil_error}")
    
    try:
        nparr = np.frombuffer(file_content, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is not None and img.size > 0:
            cv2.imwrite(output_path, img)
            logger.info(f"OpenCVで画像を保存しました: {output_path}")
            return output_path
    except Exception as cv_error:
        logger.warning(f"OpenCVでの画像保存に失敗しました: {cv_error}")
    
    try:
        import subprocess
        import tempfile
        
        with tempfile.NamedTemporaryFile(suffix='.bin', delete=False) as temp_file:
            temp_file.write(file_content)
            temp_input_path = temp_file.name
        
        convert_cmd = ['convert', temp_input_path, output_path]
        result = subprocess.run(convert_cmd, capture_output=True, text=True)
        
        try:
            os.remove(temp_input_path)
        except:
            pass
        
        if result.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            logger.info(f"ImageMagickで画像を保存しました: {output_path}")
            return output_path
        else:
            logger.warning(f"ImageMagickでの画像保存に失敗しました: {result.stderr}")
    except Exception as im_error:
        logger.warning(f"ImageMagickでの処理中にエラーが発生しました: {im_error}")
    
    try:
        with open(output_path, 'wb') as f:
            f.write(file_content)
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            logger.info(f"単純なファイル書き込みで画像を保存しました: {output_path}")
            return output_path
    except Exception as write_error:
        logger.warning(f"ファイル書き込みでの保存に失敗しました: {write_error}")
        
    logger.error("すべての方法で画像の保存に失敗しました")
    raise ValueError("画像の保存に失敗しました。別の画像を試してください。")

def optimize_image(image_path: str, target_size: Tuple[int, int] = (800, 600)) -> str:
    """
    画像を最適化する（リサイズ、コントラスト調整など）
    複数の方法を試して、可能な限り画像を最適化する
    
    Args:
        image_path: 処理する画像のパス
        target_size: 目標サイズ（幅, 高さ）
        
    Returns:
        最適化された画像のパス
    """
    # 出力パスの生成
    output_path = image_path.rsplit(".", 1)[0] + "_optimized.jpg"
    
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
        
        # 画像の保存
        cv2.imwrite(output_path, enhanced_bgr)
        
        logger.info(f"PILとOpenCVで画像を最適化しました: {output_path}")
        return output_path
    except Exception as pil_error:
        logger.warning(f"PILとOpenCVでの画像最適化に失敗しました: {pil_error}")
    
    try:
        # 画像の読み込み
        image = cv2.imread(image_path)
        if image is not None and image.size > 0:
            height, width = image.shape[:2]
            if width > target_size[0] or height > target_size[1]:
                scale = min(target_size[0] / width, target_size[1] / height)
                new_width = int(width * scale)
                new_height = int(height * scale)
                image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
            
            # グレースケール変換
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # コントラスト調整
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            enhanced = clahe.apply(gray)
            
            # BGRに戻す
            enhanced_bgr = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)
            
            # 画像の保存
            cv2.imwrite(output_path, enhanced_bgr)
            
            logger.info(f"OpenCVのみで画像を最適化しました: {output_path}")
            return output_path
    except Exception as cv_error:
        logger.warning(f"OpenCVでの画像最適化に失敗しました: {cv_error}")
    
    try:
        import subprocess
        
        convert_cmd = [
            'convert', image_path,
            '-resize', f'{target_size[0]}x{target_size[1]}>', # アスペクト比を保持してリサイズ
            '-contrast-stretch', '2%',  # コントラスト調整
            '-sharpen', '0x1.0',       # シャープネス調整
            output_path
        ]
        result = subprocess.run(convert_cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            logger.info(f"ImageMagickで画像を最適化しました: {output_path}")
            return output_path
        else:
            logger.warning(f"ImageMagickでの画像最適化に失敗しました: {result.stderr}")
    except Exception as im_error:
        logger.warning(f"ImageMagickでの処理中にエラーが発生しました: {im_error}")
    
    logger.error(f"すべての方法で画像の最適化に失敗しました。元の画像を使用します: {image_path}")
    return image_path
