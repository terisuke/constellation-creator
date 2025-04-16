import cv2
import numpy as np
from typing import List, Tuple, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def detect_stars(image_path: str, threshold: int = 200, min_area: int = 5) -> List[Dict[str, Any]]:
    """
    画像から星を検出し、座標と明るさを返す
    
    Args:
        image_path: 処理する画像のパス
        threshold: 白色を検出するための閾値（0-255）
        min_area: 星として認識する最小面積
        
    Returns:
        検出された星のリスト、各星は辞書形式で座標とサイズを含む
    """
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"画像の読み込みに失敗しました: {image_path}")
            
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        _, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        stars = []
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area >= min_area:  # 小さすぎる点はノイズとして除外
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    brightness = np.mean(gray[cy-2:cy+2, cx-2:cx+2]) if cy >= 2 and cx >= 2 else 0
                    stars.append({
                        "x": cx,
                        "y": cy,
                        "brightness": brightness,
                        "area": area
                    })
        
        logger.info(f"{len(stars)}個の星を検出しました")
        return stars
    except Exception as e:
        logger.error(f"星の検出中にエラーが発生しました: {e}")
        raise

def cluster_stars(stars: List[Dict[str, Any]], max_distance: int = 50) -> List[List[Dict[str, Any]]]:
    """
    星をクラスタリングして星座を形成するためのグループに分ける
    
    Args:
        stars: 検出された星のリスト
        max_distance: 同じクラスタとみなす星間の最大距離
        
    Returns:
        クラスタリングされた星のリスト
    """
    if not stars:
        return []
        
    sorted_stars = sorted(stars, key=lambda x: x["brightness"], reverse=True)
    
    clusters = []
    assigned = [False] * len(sorted_stars)
    
    for i, star in enumerate(sorted_stars):
        if assigned[i]:
            continue
            
        cluster = [star]
        assigned[i] = True
        
        for j, candidate in enumerate(sorted_stars):
            if assigned[j]:
                continue
                
            for s in cluster:
                distance = np.sqrt((s["x"] - candidate["x"])**2 + (s["y"] - candidate["y"])**2)
                if distance <= max_distance:
                    cluster.append(candidate)
                    assigned[j] = True
                    break
        
        clusters.append(cluster)
    
    logger.info(f"{len(clusters)}個の星座クラスタを形成しました")
    return clusters

def get_constellation_points(image_path: str) -> List[List[Tuple[int, int]]]:
    """
    画像から星座の点群を取得する
    
    Args:
        image_path: 処理する画像のパス
        
    Returns:
        星座の点群（クラスタごとの座標リスト）
    """
    stars = detect_stars(image_path)
    
    clusters = cluster_stars(stars)
    
    constellation_points = []
    for cluster in clusters:
        if len(cluster) >= 3:  # 最低3つの星があるクラスタのみ使用
            points = [(star["x"], star["y"]) for star in cluster]
            constellation_points.append(points)
    
    return constellation_points
