import os
import sys
import logging
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.star_detection import detect_stars, cluster_stars, get_constellation_points

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def visualize_stars(image_path, stars, output_path=None):
    """
    検出された星を可視化する
    
    Args:
        image_path: 元画像のパス
        stars: 検出された星のリスト
        output_path: 出力画像のパス（指定がない場合は表示のみ）
    """
    try:
        image = cv2.imread(image_path)
        if image is None:
            pil_image = Image.open(image_path)
            if pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')
            image_np = np.array(pil_image)
            image = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    except Exception as e:
        logger.error(f"画像の読み込みに失敗しました: {e}")
        image = np.zeros((600, 800, 3), dtype=np.uint8)
    
    for star in stars:
        x, y = star["x"], star["y"]
        brightness = star["brightness"]
        area = star["area"]
        
        radius = max(3, int(np.sqrt(area / np.pi)))
        
        color = (255, 255, 255)
        
        cv2.circle(image, (x, y), radius, color, -1)
        
        cv2.putText(
            image, 
            f"{int(brightness)}", 
            (x + radius + 2, y), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            0.4, 
            (0, 255, 255), 
            1
        )
    
    if output_path:
        cv2.imwrite(output_path, image)
        logger.info(f"可視化結果を保存しました: {output_path}")
    
    return image

def visualize_clusters(image_path, clusters, output_path=None):
    """
    クラスタリングされた星を可視化する
    
    Args:
        image_path: 元画像のパス
        clusters: クラスタリングされた星のリスト
        output_path: 出力画像のパス（指定がない場合は表示のみ）
    """
    try:
        image = cv2.imread(image_path)
        if image is None:
            pil_image = Image.open(image_path)
            if pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')
            image_np = np.array(pil_image)
            image = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    except Exception as e:
        logger.error(f"画像の読み込みに失敗しました: {e}")
        image = np.zeros((600, 800, 3), dtype=np.uint8)
    
    colors = [
        (255, 0, 0),    # 赤
        (0, 255, 0),    # 緑
        (0, 0, 255),    # 青
        (255, 255, 0),  # 黄
        (255, 0, 255),  # マゼンタ
        (0, 255, 255),  # シアン
        (255, 128, 0),  # オレンジ
        (128, 0, 255),  # 紫
        (0, 128, 255),  # 水色
        (128, 255, 0)   # 黄緑
    ]
    
    for i, cluster in enumerate(clusters):
        color = colors[i % len(colors)]
        
        for star in cluster:
            x, y = star["x"], star["y"]
            brightness = star["brightness"]
            area = star["area"]
            
            radius = max(3, int(np.sqrt(area / np.pi)))
            
            cv2.circle(image, (x, y), radius, color, -1)
        
        for j in range(len(cluster) - 1):
            pt1 = (cluster[j]["x"], cluster[j]["y"])
            pt2 = (cluster[j+1]["x"], cluster[j+1]["y"])
            cv2.line(image, pt1, pt2, color, 2)
    
    if output_path:
        cv2.imwrite(output_path, image)
        logger.info(f"クラスタ可視化結果を保存しました: {output_path}")
    
    return image

def test_star_detection():
    """
    星検出機能をテストする
    """
    sample_path = "../frontend/public/sample.jpg"
    
    if not os.path.exists(sample_path):
        logger.error(f"サンプル画像が見つかりません: {sample_path}")
        return
    
    logger.info(f"サンプル画像を使用してテスト: {sample_path}")
    
    stars = detect_stars(
        sample_path, 
        use_adaptive_threshold=True, 
        use_blob_detection=True
    )
    logger.info(f"{len(stars)}個の星を検出しました")
    
    stars_output_path = "/tmp/detected_stars.jpg"
    visualize_stars(sample_path, stars, stars_output_path)
    
    clusters = cluster_stars(stars, max_distance=50, min_stars=3, max_stars=12)
    logger.info(f"{len(clusters)}個のクラスタを形成しました")
    
    clusters_output_path = "/tmp/star_clusters.jpg"
    visualize_clusters(sample_path, clusters, clusters_output_path)
    
    constellation_points = get_constellation_points(sample_path)
    logger.info(f"{len(constellation_points)}個の星座を形成しました")
    
    logger.info(f"検出された星: {len(stars)}個")
    logger.info(f"形成されたクラスタ: {len(clusters)}個")
    logger.info(f"生成された星座: {len(constellation_points)}個")
    
    logger.info(f"検出結果の可視化: {stars_output_path}")
    logger.info(f"クラスタリング結果の可視化: {clusters_output_path}")
    
    return stars, clusters, constellation_points

if __name__ == "__main__":
    test_star_detection()
