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
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        
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
            output_path = image_path.rsplit(".", 1)[0] + "_constellation." + image_path.rsplit(".", 1)[1]
        
        image.save(output_path)
        logger.info(f"星座画像を保存しました: {output_path}")
        
        return output_path
    except Exception as e:
        logger.error(f"星座線の描画中にエラーが発生しました: {e}")
        raise
