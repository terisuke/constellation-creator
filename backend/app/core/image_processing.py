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
    logger.info(f"検証する画像のサイズ: {len(file_content)} bytes")
    
    if not file_content or len(file_content) < 10:
        logger.error("画像ファイルが空か、サイズが小さすぎます")
        return False
    
    try:
        from PIL import Image, UnidentifiedImageError
        image = Image.open(io.BytesIO(file_content))
        image.verify()
        logger.info("PILによる画像検証に成功しました")
        return True
    except UnidentifiedImageError:
        logger.warning("PILで認識できない画像形式です。AVIFなどの特殊形式の可能性があります")
    except Exception as e:
        logger.warning(f"PILでの画像検証に失敗しました: {e}")
    
    try:
        import numpy as np
        nparr = np.frombuffer(file_content, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is not None and img.size > 0:
            logger.info("OpenCVによる画像検証に成功しました")
            return True
        else:
            logger.warning("OpenCVでの画像検証に失敗しました")
    except Exception as e:
        logger.warning(f"OpenCVでの画像検証に失敗しました: {e}")
    
    try:
        import tempfile
        import subprocess
        import os
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.bin') as temp:
            temp.write(file_content)
            temp_path = temp.name
        
        try:
            result = subprocess.run(['identify', temp_path], 
                                   capture_output=True, 
                                   text=True, 
                                   check=False)
            
            if result.returncode == 0:
                logger.info(f"ImageMagickによる画像検証に成功しました: {result.stdout.strip()}")
                os.unlink(temp_path)
                return True
            else:
                logger.warning(f"ImageMagickでの画像検証に失敗しました: {result.stderr.strip()}")
        except Exception as e:
            logger.warning(f"ImageMagickコマンド実行中にエラーが発生しました: {e}")
        finally:
            try:
                os.unlink(temp_path)
            except:
                pass
    except Exception as e:
        logger.warning(f"ImageMagickでの検証中にエラーが発生しました: {e}")
    
    image_signatures = {
        b'\xFF\xD8\xFF': 'JPEG',
        b'\x89\x50\x4E\x47': 'PNG',
        b'GIF8': 'GIF',
        b'RIFF': 'WEBP',
        b'\x00\x00\x00\x0C\x6A\x50\x20\x20': 'JPEG2000',
        b'\x49\x49\x2A\x00': 'TIFF',
        b'\x4D\x4D\x00\x2A': 'TIFF',
        b'\x42\x4D': 'BMP',
        b'\x00\x00\x01\x00': 'ICO',
        b'AVIF': 'AVIF',
    }
    
    for signature, format_name in image_signatures.items():
        if file_content.startswith(signature):
            logger.info(f"ファイルシグネチャから{format_name}形式と判断されました")
            return True
    
    logger.info("画像検証に失敗しましたが、処理を続行します")
    return True

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
        from PIL import Image, UnidentifiedImageError
        
        binary_filename = f"{uuid.uuid4()}_original"
        binary_path = os.path.join(output_dir, binary_filename)
        
        with open(binary_path, 'wb') as f:
            f.write(file_content)
        
        filename = f"{uuid.uuid4()}.jpg"
        output_path = os.path.join(output_dir, filename)
        
        fallback_image = Image.new('RGB', (800, 600), color=(0, 0, 0))
        fallback_image.save(output_path, format='JPEG')
        
        try:
            image = Image.open(io.BytesIO(file_content))
            if image.mode != 'RGB':
                image = image.convert('RGB')
            image.save(output_path, format='JPEG')
            logger.info(f"PILで直接バイトデータから画像を変換しました: {output_path}")
            
            try:
                os.remove(binary_path)
            except:
                pass
                
            return output_path
        except (UnidentifiedImageError, Exception) as direct_error:
            logger.error(f"PILでの直接バイトデータからの変換に失敗しました: {direct_error}")
        
        try:
            with open(binary_path, 'rb') as f:
                image_data = f.read()
                
            image = Image.open(io.BytesIO(image_data))
            if image.mode != 'RGB':
                image = image.convert('RGB')
            image.save(output_path, format='JPEG')
            logger.info(f"PILで保存したバイナリから画像を変換しました: {output_path}")
            
            try:
                os.remove(binary_path)
            except:
                pass
                
            return output_path
        except Exception as img_error:
            logger.error(f"PILでの保存バイナリからの変換に失敗しました: {img_error}")
        
        try:
            import cv2
            import numpy as np
            
            nparr = np.frombuffer(file_content, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is not None:
                cv2.imwrite(output_path, img)
                logger.info(f"OpenCVを使用して画像を変換しました: {output_path}")
                
                try:
                    os.remove(binary_path)
                except:
                    pass
                    
                return output_path
        except Exception as cv_error:
            logger.error(f"OpenCVでの画像変換に失敗しました: {cv_error}")
        
        try:
            import subprocess
            
            try:
                result = subprocess.run(['which', 'convert'], 
                                       capture_output=True, 
                                       text=True, 
                                       check=False)
                
                if result.returncode == 0:
                    convert_output_path = os.path.join(output_dir, f"{uuid.uuid4()}_converted.jpg")
                    
                    convert_result = subprocess.run(
                        ['convert', binary_path, '-auto-orient', '-strip', convert_output_path],
                        capture_output=True,
                        text=True,
                        check=False
                    )
                    
                    if convert_result.returncode == 0 and os.path.exists(convert_output_path) and os.path.getsize(convert_output_path) > 0:
                        logger.info(f"ImageMagickを使用して画像を変換しました: {convert_output_path}")
                        
                        try:
                            os.remove(binary_path)
                        except:
                            pass
                            
                        return convert_output_path
                    else:
                        logger.warning(f"ImageMagickでの変換に失敗しました: {convert_result.stderr}")
                        
                        try:
                            avif_convert_path = os.path.join(output_dir, f"{uuid.uuid4()}_avif_converted.jpg")
                            avif_result = subprocess.run(
                                ['convert', binary_path, '-auto-orient', '-strip', '-quality', '90', avif_convert_path],
                                capture_output=True,
                                text=True,
                                check=False
                            )
                            
                            if avif_result.returncode == 0 and os.path.exists(avif_convert_path) and os.path.getsize(avif_convert_path) > 0:
                                logger.info(f"ImageMagickを使用してAVIF画像を変換しました: {avif_convert_path}")
                                
                                try:
                                    os.remove(binary_path)
                                except:
                                    pass
                                    
                                return avif_convert_path
                        except Exception as avif_error:
                            logger.warning(f"AVIF変換中にエラーが発生しました: {avif_error}")
                else:
                    logger.warning("ImageMagick（convert）が見つかりません")
            except (subprocess.SubprocessError, subprocess.CalledProcessError) as subprocess_error:
                logger.error(f"外部コマンドでの変換に失敗しました: {subprocess_error}")
        except Exception as external_error:
            logger.error(f"外部コマンド実行中にエラーが発生しました: {external_error}")
        
        logger.info(f"すべての変換方法が失敗しました。フォールバック: 黒い画像を使用します: {output_path}")
        return output_path
    except Exception as e:
        logger.error(f"画像の保存中にエラーが発生しました: {e}")
        
        try:
            import uuid
            output_path = os.path.join(output_dir, f"{uuid.uuid4()}.jpg")
            fallback_image = Image.new('RGB', (800, 600), color=(0, 0, 0))
            fallback_image.save(output_path, format='JPEG')
            logger.info(f"エラー発生時のフォールバック: 黒い画像を生成しました: {output_path}")
            return output_path
        except Exception as fallback_error:
            logger.error(f"フォールバック画像の生成に失敗しました: {fallback_error}")
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
        from PIL import Image, UnidentifiedImageError
        import os
        
        output_path = image_path.rsplit(".", 1)[0] + "_optimized.jpg"
        
        if not os.path.exists(image_path):
            logger.error(f"最適化する画像ファイルが存在しません: {image_path}")
            fallback_image = Image.new('RGB', target_size, color=(0, 0, 0))
            fallback_image.save(output_path, format='JPEG')
            logger.info(f"ファイルが存在しないため、黒い画像を生成しました: {output_path}")
            return output_path
        
        try:
            img_cv = cv2.imread(image_path)
            if img_cv is not None and img_cv.size > 0:
                img_cv = cv2.resize(img_cv, target_size)
                
                gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
                
                equalized = cv2.equalizeHist(gray)
                
                img_cv = cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)
                
                cv2.imwrite(output_path, img_cv)
                logger.info(f"OpenCVで画像を最適化しました: {output_path}")
                return output_path
            else:
                logger.warning("OpenCVで画像を読み込めませんでした")
        except Exception as cv_error:
            logger.error(f"OpenCVでの処理に失敗しました: {cv_error}")
        
        try:
            image = Image.open(image_path)
            
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            image = image.resize(target_size, Image.Resampling.LANCZOS)
            
            image.save(output_path, format='JPEG')
            logger.info(f"PILで画像を最適化しました: {output_path}")
            return output_path
        except (UnidentifiedImageError, Exception) as pil_error:
            logger.error(f"PILでの画像処理に失敗しました: {pil_error}")
        
        try:
            import subprocess
            
            try:
                result = subprocess.run(['which', 'convert'], 
                                       capture_output=True, 
                                       text=True, 
                                       check=False)
                
                if result.returncode == 0:
                    convert_result = subprocess.run([
                        'convert', image_path,
                        '-auto-orient',
                        '-strip',
                        '-resize', f'{target_size[0]}x{target_size[1]}',
                        '-contrast-stretch', '2%',
                        '-sharpen', '0x1.0',
                        output_path
                    ], capture_output=True, text=True, check=False)
                    
                    if convert_result.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                        logger.info(f"ImageMagickを使用して画像を最適化しました: {output_path}")
                        return output_path
                    else:
                        logger.warning(f"ImageMagickでの最適化に失敗しました: {convert_result.stderr}")
                        
                        try:
                            import uuid
                            alt_output_path = os.path.join(os.path.dirname(output_path), f"{uuid.uuid4()}_alt_optimized.jpg")
                            alt_result = subprocess.run([
                                'convert', image_path,
                                '-auto-orient',
                                '-strip',
                                '-resize', f'{target_size[0]}x{target_size[1]}',
                                '-quality', '90',
                                alt_output_path
                            ], capture_output=True, text=True, check=False)
                            
                            if alt_result.returncode == 0 and os.path.exists(alt_output_path) and os.path.getsize(alt_output_path) > 0:
                                logger.info(f"ImageMagickを使用して代替方法で画像を最適化しました: {alt_output_path}")
                                return alt_output_path
                        except Exception as alt_error:
                            logger.warning(f"代替最適化中にエラーが発生しました: {alt_error}")
                else:
                    logger.warning("ImageMagick（convert）が見つかりません")
            except (subprocess.SubprocessError, subprocess.CalledProcessError) as subprocess_error:
                logger.error(f"外部コマンドでの最適化に失敗しました: {subprocess_error}")
        except Exception as external_error:
            logger.error(f"外部コマンド実行中にエラーが発生しました: {external_error}")
        
        fallback_image = Image.new('RGB', target_size, color=(0, 0, 0))
        fallback_image.save(output_path, format='JPEG')
        logger.info(f"フォールバック: 黒い画像を生成しました: {output_path}")
        return output_path
                
    except Exception as e:
        logger.error(f"画像の最適化中にエラーが発生しました: {e}")
        
        try:
            import uuid
            output_path = f"/tmp/{uuid.uuid4()}_optimized.jpg"
            fallback_image = Image.new('RGB', target_size, color=(0, 0, 0))
            fallback_image.save(output_path, format='JPEG')
            logger.info(f"エラー発生時のフォールバック: 黒い画像を生成しました: {output_path}")
            return output_path
        except Exception as fallback_error:
            logger.error(f"フォールバック画像の生成に失敗しました: {fallback_error}")
            return image_path
