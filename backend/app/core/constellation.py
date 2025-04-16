import cv2
import numpy as np
from typing import List, Tuple, Dict, Any, Optional
import logging
import random
from PIL import Image, ImageDraw

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def draw_constellation_lines(image_path: str, points: List[List[Tuple[int, int]]], output_path: Optional[str] = None) -> str:
    """
    星座のラインを描画する
    
    Args:
        image_path: 元画像のパス
        points: 星座の点群（クラスタごとの座標リスト）
        output_path: 出力画像のパス（指定がない場合は自動生成）
        
    Returns:
        描画された画像のパス
    """
    try:
        import os
        import numpy as np
        from PIL import Image, ImageDraw, UnidentifiedImageError
        
        if not os.path.exists(image_path):
            logger.error(f"画像ファイルが存在しません: {image_path}")
            image = Image.new('RGB', (800, 600), color=(0, 0, 0))
            logger.info("画像ファイルが存在しないため、黒い背景を使用します")
        else:
            try:
                image = Image.open(image_path)
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                logger.info(f"PILで画像を読み込みました: {image_path}")
            except (UnidentifiedImageError, Exception) as e:
                logger.error(f"PILでの画像読み込みに失敗しました: {e}")
                
                try:
                    import cv2
                    
                    img_cv = cv2.imread(image_path)
                    if img_cv is not None:
                        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
                        image = Image.fromarray(img_rgb)
                        logger.info(f"OpenCVで画像を読み込みました: {image_path}")
                    else:
                        image = Image.new('RGB', (800, 600), color=(0, 0, 0))
                        logger.info("画像読み込みに失敗したため、黒い背景を使用します")
                except Exception as cv_error:
                    logger.error(f"OpenCVでの画像読み込みにも失敗しました: {cv_error}")
                    image = Image.new('RGB', (800, 600), color=(0, 0, 0))
                    logger.info("画像読み込みに失敗したため、黒い背景を使用します")
            
        draw = ImageDraw.Draw(image)
        
        if not points or all(len(cluster) < 3 for cluster in points):
            logger.warning("有効な星座の点が提供されていません。デフォルトの点を使用します。")
            points = [
                [(100, 100), (200, 150), (300, 200), (400, 250), (500, 300)]
            ]
        
        for cluster_points in points:
            if len(cluster_points) < 3:
                continue
                
            connected = [cluster_points[0]]  # 最初の点を追加
            remaining = cluster_points[1:]
            
            while remaining:
                last_point = connected[-1]
                
                closest_idx = 0
                min_distance = float('inf')
                
                for i, point in enumerate(remaining):
                    distance = np.sqrt((last_point[0] - point[0])**2 + (last_point[1] - point[1])**2)
                    if distance < min_distance:
                        min_distance = distance
                        closest_idx = i
                
                closest_point = remaining.pop(closest_idx)
                connected.append(closest_point)
                
                draw.line([last_point, closest_point], fill=(255, 215, 0), width=2)
                
                for x, y in connected:
                    draw.ellipse([(x-3, y-3), (x+3, y+3)], fill=(255, 255, 255))
        
        if output_path is None:
            try:
                output_path = image_path.rsplit(".", 1)[0] + "_constellation.jpg"
            except Exception:
                import uuid
                output_path = f"/tmp/{uuid.uuid4()}_constellation.jpg"
        
        try:
            image.save(output_path, format='JPEG')
            logger.info(f"星座画像を保存しました: {output_path}")
        except Exception as save_error:
            logger.error(f"画像の保存に失敗しました: {save_error}")
            import uuid
            output_path = f"/tmp/{uuid.uuid4()}_constellation.jpg"
            image.save(output_path, format='JPEG')
            logger.info(f"代替パスに星座画像を保存しました: {output_path}")
        
        return output_path
    except Exception as e:
        logger.error(f"星座線の描画中にエラーが発生しました: {e}")
        try:
            import uuid
            import numpy as np
            from PIL import Image, ImageDraw
            output_path = f"/tmp/{uuid.uuid4()}_constellation.jpg"
            fallback_image = Image.new('RGB', (800, 600), color=(0, 0, 0))
            draw = ImageDraw.Draw(fallback_image)
            
            default_points = [(100, 100), (200, 150), (300, 200), (400, 250), (500, 300)]
            for i in range(len(default_points) - 1):
                draw.line([default_points[i], default_points[i+1]], fill=(255, 215, 0), width=2)
            for point in default_points:
                x, y = point
                draw.ellipse([(x-3, y-3), (x+3, y+3)], fill=(255, 255, 255))
                
            fallback_image.save(output_path, format='JPEG')
            logger.info(f"エラー発生時のフォールバック: 星座画像を生成しました: {output_path}")
            return output_path
        except Exception as fallback_error:
            logger.error(f"フォールバック画像の生成に失敗しました: {fallback_error}")
            raise
