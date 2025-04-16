import cv2
import numpy as np
from typing import List, Tuple, Dict, Any, Optional
import logging
import os
from PIL import Image, UnidentifiedImageError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def detect_stars(image_path: str, threshold: Optional[int] = None, min_area: int = 5, 
                 use_adaptive_threshold: bool = True, use_blob_detection: bool = True) -> List[Dict[str, Any]]:
    """
    画像から星を検出し、座標と明るさを返す
    
    Args:
        image_path: 処理する画像のパス
        threshold: 白色を検出するための閾値（0-255）、Noneの場合は自動設定
        min_area: 星として認識する最小面積
        use_adaptive_threshold: 適応的閾値処理を使用するかどうか
        use_blob_detection: Blob検出を使用するかどうか
        
    Returns:
        検出された星のリスト、各星は辞書形式で座標とサイズを含む
    """
    default_stars = [
        {"x": 100, "y": 100, "brightness": 200, "area": 10},
        {"x": 200, "y": 150, "brightness": 180, "area": 8},
        {"x": 300, "y": 200, "brightness": 220, "area": 12},
        {"x": 400, "y": 250, "brightness": 190, "area": 9},
        {"x": 500, "y": 300, "brightness": 210, "area": 11}
    ]
    
    try:
        if not os.path.exists(image_path):
            logger.error(f"画像ファイルが存在しません: {image_path}")
            return default_stars
        
        image = load_image(image_path)
        if image is None:
            logger.error(f"画像の読み込みに失敗しました: {image_path}")
            return default_stars
            
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        stars = []
        
        if use_blob_detection:
            blob_stars = detect_stars_with_blob(gray)
            if blob_stars:
                stars.extend(blob_stars)
                logger.info(f"Blob検出で{len(blob_stars)}個の星を検出しました")
        
        if len(stars) < 10:
            threshold_stars = detect_stars_with_threshold(gray, threshold, min_area, use_adaptive_threshold)
            if threshold_stars:
                for star in threshold_stars:
                    if not any(is_close_to_existing_star(star, existing_star, 10) for existing_star in stars):
                        stars.append(star)
                logger.info(f"閾値処理で{len(threshold_stars)}個の星を検出しました")
        
        if not stars:
            logger.warning(f"星が検出されませんでした。デフォルトの星を使用します: {image_path}")
            return default_stars
        
        stars = sorted(stars, key=lambda x: x["brightness"], reverse=True)
        
        if len(stars) > 200:
            stars = stars[:200]
            
        logger.info(f"合計{len(stars)}個の星を検出しました")
        return stars
    except Exception as e:
        logger.error(f"星の検出中にエラーが発生しました: {e}")
        return default_stars

def load_image(image_path: str) -> Optional[np.ndarray]:
    """
    複数の方法を試して画像を読み込む
    AVIF、HEIC、WebPなどの特殊な形式にも対応
    
    Args:
        image_path: 画像ファイルのパス
        
    Returns:
        読み込まれた画像（OpenCV形式）、失敗した場合はNone
    """
    logger.info(f"画像の読み込みを開始します: {image_path}")
    
    try:
        pil_image = Image.open(image_path)
        logger.info(f"PILで画像を開きました: フォーマット={pil_image.format}, サイズ={pil_image.size}, モード={pil_image.mode}")
        
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
            logger.info(f"画像をRGBモードに変換しました")
            
        image_np = np.array(pil_image)
        image = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        logger.info(f"PILで画像を正常に読み込みました: {image_path}")
        return image
    except (UnidentifiedImageError, Exception) as pil_error:
        logger.warning(f"PILでの画像読み込みに失敗しました: {pil_error}")
    
    try:
        image = cv2.imread(image_path)
        if image is not None and image.size > 0:
            height, width = image.shape[:2]
            logger.info(f"OpenCVで画像を読み込みました: {image_path}, サイズ={width}x{height}")
            return image
        else:
            logger.warning(f"OpenCVでの画像読み込みに失敗しました: 画像データがNoneまたは空です")
    except Exception as cv_error:
        logger.warning(f"OpenCVでの画像読み込みに失敗しました: {cv_error}")
    
    try:
        import subprocess
        import tempfile
        import uuid
        
        temp_dir = tempfile.gettempdir()
        temp_filename = f"converted_{uuid.uuid4()}.jpg"
        temp_path = os.path.join(temp_dir, temp_filename)
        
        convert_cmd = ['convert', image_path, '-auto-orient', '-strip', temp_path]
        logger.info(f"ImageMagickで変換を試みます: {' '.join(convert_cmd)}")
        
        result = subprocess.run(convert_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info(f"ImageMagickで画像を変換しました: {image_path} -> {temp_path}")
            
            try:
                converted_image = cv2.imread(temp_path)
                if converted_image is not None and converted_image.size > 0:
                    height, width = converted_image.shape[:2]
                    logger.info(f"変換された画像を読み込みました: {temp_path}, サイズ={width}x{height}")
                    
                    try:
                        os.remove(temp_path)
                        logger.info(f"一時ファイルを削除しました: {temp_path}")
                    except Exception as rm_error:
                        logger.warning(f"一時ファイルの削除に失敗しました: {rm_error}")
                    
                    return converted_image
                else:
                    logger.warning(f"変換された画像の読み込みに失敗しました: 画像データがNoneまたは空です")
            except Exception as read_error:
                logger.warning(f"変換された画像の読み込みに失敗しました: {read_error}")
        else:
            logger.warning(f"ImageMagickでの変換に失敗しました: {result.stderr}")
            
            try:
                special_convert_cmd = [
                    'convert', image_path, 
                    '-auto-orient', '-strip', 
                    '-define', 'heif:preserve-orientation=true',
                    '-define', 'avif:preserve-orientation=true',
                    temp_path
                ]
                logger.info(f"特殊オプションでImageMagickによる変換を再試行します")
                
                special_result = subprocess.run(special_convert_cmd, capture_output=True, text=True)
                
                if special_result.returncode == 0:
                    logger.info(f"特殊オプションでImageMagickによる変換に成功しました")
                    
                    converted_image = cv2.imread(temp_path)
                    if converted_image is not None and converted_image.size > 0:
                        try:
                            os.remove(temp_path)
                        except:
                            pass
                        
                        return converted_image
            except Exception as special_error:
                logger.warning(f"特殊オプションでの変換にも失敗しました: {special_error}")
    except Exception as im_error:
        logger.warning(f"ImageMagickでの処理中にエラーが発生しました: {im_error}")
    
    try:
        with open(image_path, 'rb') as f:
            binary_data = f.read()
            
        nparr = np.frombuffer(binary_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is not None and img.size > 0:
            height, width = img.shape[:2]
            logger.info(f"バイナリデータから直接画像を読み込みました: {image_path}, サイズ={width}x{height}")
            return img
        else:
            logger.warning("バイナリデータからの画像読み込みに失敗しました")
    except Exception as bin_error:
        logger.warning(f"バイナリデータからの読み込みに失敗しました: {bin_error}")
    
    logger.error(f"すべての方法で画像の読み込みに失敗しました: {image_path}")
    return None

def is_close_to_existing_star(star1: Dict[str, Any], star2: Dict[str, Any], min_distance: int) -> bool:
    """
    2つの星が近すぎるかどうかを判定
    
    Args:
        star1: 1つ目の星
        star2: 2つ目の星
        min_distance: 最小距離
        
    Returns:
        近すぎる場合はTrue
    """
    distance = np.sqrt((star1["x"] - star2["x"])**2 + (star1["y"] - star2["y"])**2)
    return distance < min_distance

def detect_stars_with_blob(gray_image: np.ndarray) -> List[Dict[str, Any]]:
    """
    Blob検出を使用して星を検出
    
    Args:
        gray_image: グレースケール画像
        
    Returns:
        検出された星のリスト
    """
    params = cv2.SimpleBlobDetector_Params()
    
    params.filterByColor = True
    params.blobColor = 255
    
    params.filterByArea = True
    params.minArea = 3
    params.maxArea = 300
    
    params.filterByCircularity = True
    params.minCircularity = 0.5
    
    params.filterByConvexity = True
    params.minConvexity = 0.5
    
    params.filterByInertia = True
    params.minInertiaRatio = 0.3
    
    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(gray_image)
    
    stars = []
    for kp in keypoints:
        x, y = int(kp.pt[0]), int(kp.pt[1])
        size = kp.size
        x_min, x_max = max(0, x-2), min(gray_image.shape[1]-1, x+2)
        y_min, y_max = max(0, y-2), min(gray_image.shape[0]-1, y+2)
        brightness = np.mean(gray_image[y_min:y_max+1, x_min:x_max+1])
        
        stars.append({
            "x": x,
            "y": y,
            "brightness": brightness,
            "area": size * size * np.pi / 4  # 円の面積の近似
        })
    
    return stars

def detect_stars_with_threshold(gray_image: np.ndarray, threshold: Optional[int] = None, 
                               min_area: int = 5, use_adaptive: bool = True) -> List[Dict[str, Any]]:
    """
    閾値処理を使用して星を検出
    
    Args:
        gray_image: グレースケール画像
        threshold: 閾値（Noneの場合は自動設定）
        min_area: 最小面積
        use_adaptive: 適応的閾値処理を使用するかどうか
        
    Returns:
        検出された星のリスト
    """
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray_image)
    
    if use_adaptive:
        thresh = cv2.adaptiveThreshold(
            enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, -2
        )
    else:
        if threshold is None:
            threshold, _ = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        _, thresh = cv2.threshold(enhanced, threshold, 255, cv2.THRESH_BINARY)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 検出された星のリスト
    stars = []
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if area >= min_area:  # 小さすぎる点はノイズとして除外
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                
                x_min, x_max = max(0, cx-2), min(gray_image.shape[1]-1, cx+2)
                y_min, y_max = max(0, cy-2), min(gray_image.shape[0]-1, cy+2)
                brightness = np.mean(gray_image[y_min:y_max+1, x_min:x_max+1])
                
                stars.append({
                    "x": cx,
                    "y": cy,
                    "brightness": brightness,
                    "area": area
                })
    
    return stars

def cluster_stars(stars: List[Dict[str, Any]], max_distance: int = 50, 
                        min_stars: int = 3, max_stars: int = 12) -> List[List[Dict[str, Any]]]:
    """
    星をクラスタリングして星座を形成するためのグループに分ける
    
    Args:
        stars: 検出された星のリスト
        max_distance: 同じクラスタとみなす星間の最大距離
        min_stars: クラスタあたりの最小星数
        max_stars: クラスタあたりの最大星数
        
    Returns:
        クラスタリングされた星のリスト
    """
    if not stars:
        default_stars = [
            {"x": 100, "y": 100, "brightness": 200, "area": 10},
            {"x": 200, "y": 150, "brightness": 180, "area": 8},
            {"x": 300, "y": 200, "brightness": 220, "area": 12},
            {"x": 400, "y": 250, "brightness": 190, "area": 9},
            {"x": 500, "y": 300, "brightness": 210, "area": 11}
        ]
        return [default_stars]
    
    adaptive_min_stars = min(min_stars, max(2, len(stars) // 2))
    logger.info(f"適応的な最小星数: {adaptive_min_stars}（元の設定: {min_stars}）")
    
    sorted_stars = sorted(stars, key=lambda x: x["brightness"], reverse=True)
    
    clusters = []
    assigned = [False] * len(sorted_stars)
    
    for i, seed_star in enumerate(sorted_stars):
        if assigned[i]:
            continue
            
        cluster = [seed_star]
        assigned[i] = True
        
        while len(cluster) < max_stars:
            nearest_star = None
            min_dist = float('inf')
            nearest_idx = -1
            
            for j, candidate in enumerate(sorted_stars):
                if assigned[j]:
                    continue
                    
                for s in cluster:
                    dist = np.sqrt((s["x"] - candidate["x"])**2 + (s["y"] - candidate["y"])**2)
                    if dist < min_dist and dist <= max_distance:
                        min_dist = dist
                        nearest_star = candidate
                        nearest_idx = j
            
            if nearest_star is None:
                break
                
            cluster.append(nearest_star)
            assigned[nearest_idx] = True
        
        if len(cluster) >= adaptive_min_stars:
            clusters.append(cluster)
    
    if not clusters and any(not a for a in assigned):
        unassigned_stars = [star for i, star in enumerate(sorted_stars) if not assigned[i]]
        unassigned_stars = sorted(unassigned_stars, key=lambda x: x["brightness"], reverse=True)
        
        if len(unassigned_stars) >= 2:
            new_cluster = unassigned_stars[:min(max_stars, len(unassigned_stars))]
            clusters.append(new_cluster)
            unassigned_stars = unassigned_stars[len(new_cluster):]
    
    if not clusters and stars:
        logger.warning("クラスタが形成されなかったため、すべての星を1つのクラスタとして扱います")
        clusters.append(sorted_stars[:min(max_stars, len(sorted_stars))])
    
    for i in range(len(clusters)):
        clusters[i] = sorted(clusters[i], key=lambda x: x["brightness"], reverse=True)
    
    logger.info(f"{len(clusters)}個の星座クラスタを形成しました")
    return clusters

def get_constellation_points(image_path: str, min_stars: int = 3, 
                                   max_distance: int = 50) -> List[List[Tuple[int, int]]]:
    """
    画像から星座の点群を取得する
    
    Args:
        image_path: 処理する画像のパス
        min_stars: 星座あたりの最小星数
        max_distance: 同じ星座とみなす星間の最大距離
        
    Returns:
        星座の点群（クラスタごとの座標リスト）
    """
    stars = detect_stars(
        image_path, 
        use_adaptive_threshold=True, 
        use_blob_detection=True
    )
    
    clusters = cluster_stars(
        stars, 
        max_distance=max_distance, 
        min_stars=min_stars
    )
    
    constellation_points = []
    for cluster in clusters:
        if len(cluster) >= min_stars:
            points = [(star["x"], star["y"]) for star in cluster]
            constellation_points.append(points)
    
    if len(constellation_points) == 0:
        logger.warning("有効な星座が検出されませんでした。デフォルトの星座を使用します。")
        default_points = [
            [(100, 100), (200, 150), (300, 200), (400, 250), (500, 300)],
            [(150, 400), (250, 350), (350, 300), (450, 250), (550, 200)]
        ]
        constellation_points = default_points
    
    return constellation_points

def calculate_matching_score(features: dict, cluster: list) -> float:
    """
    星座の特徴とクラスタのマッチングスコアを計算する
    
    Args:
        features: 星座の特徴
        cluster: 星のクラスタ
        
    Returns:
        マッチングスコア（0-1の範囲）
    """
    score = 0.0
    
    star_count_match = min(len(cluster) / features["star_count"], 
                          features["star_count"] / len(cluster))
    score += star_count_match * 0.3
    
    avg_brightness = sum(star["brightness"] for star in cluster) / len(cluster)
    if features["brightness"] == "high" and avg_brightness > 200:
        score += 0.2
    elif features["brightness"] == "medium" and 100 <= avg_brightness <= 200:
        score += 0.2
    elif features["brightness"] == "low" and avg_brightness < 100:
        score += 0.2
    
    if features["pattern"] == "scattered":
        xs = [star["x"] for star in cluster]
        ys = [star["y"] for star in cluster]
        if len(cluster) >= 5 and np.std(xs) > 50 and np.std(ys) > 50:
            score += 0.2
    elif features["pattern"] == "linear":
        xs = [star["x"] for star in cluster]
        ys = [star["y"] for star in cluster]
        if len(cluster) >= 3:
            try:
                from sklearn.linear_model import LinearRegression
                X = np.array(xs).reshape(-1, 1)
                y = np.array(ys)
                model = LinearRegression().fit(X, y)
                r2 = model.score(X, y)
                if r2 > 0.7:  # R^2が0.7以上なら線形と見なす
                    score += 0.2
            except:
                if len(cluster) >= 3:
                    x1, y1 = xs[0], ys[0]
                    x2, y2 = xs[-1], ys[-1]
                    distances = []
                    for i in range(1, len(xs) - 1):
                        numerator = abs((y2-y1)*xs[i] - (x2-x1)*ys[i] + x2*y1 - y2*x1)
                        denominator = ((y2-y1)**2 + (x2-x1)**2)**0.5
                        distance = numerator / denominator if denominator != 0 else 0
                        distances.append(distance)
                    if sum(distances) / len(distances) < 20:  # 平均距離が小さければ線形と見なす
                        score += 0.2
    elif features["pattern"] == "dense":
        if len(cluster) >= 5:
            xs = [star["x"] for star in cluster]
            ys = [star["y"] for star in cluster]
            if np.std(xs) < 30 and np.std(ys) < 30:
                score += 0.2
    
    
    return min(score, 1.0)

def match_constellation_with_clusters(name: str, story: str, clusters: List[List[Dict[str, Any]]]) -> Optional[int]:
    """
    星座名とストーリーから最適なクラスタを選択する
    
    Args:
        name: 星座名
        story: 星座のストーリー
        clusters: 星のクラスタのリスト
        
    Returns:
        最適なクラスタのインデックス、クラスタが空の場合でもデフォルト値0を返す
    """
    if not clusters:
        logger.warning("クラスタが空のため、デフォルトのクラスタインデックス0を返します")
        return 0  # クラスタが空の場合でもデフォルト値を返す
        
    from app.services.openai_service import extract_constellation_features
    
    try:
        features = extract_constellation_features(name, story)
        
        scores = []
        for i, cluster in enumerate(clusters):
            if len(cluster) < 3:  # 最低3つの星が必要
                scores.append((i, 0.0))
                continue
                
            score = calculate_matching_score(features, cluster)
            scores.append((i, score))
        
        if not scores:
            logger.warning("スコアが計算できなかったため、デフォルトのクラスタインデックス0を返します")
            return 0  # スコアが計算できない場合でもデフォルト値を返す
            
        selected_cluster_index = max(scores, key=lambda x: x[1])[0]
        logger.info(f"選択されたクラスタ: {selected_cluster_index}, スコア: {max(scores, key=lambda x: x[1])[1]}")
        
        return selected_cluster_index
    except Exception as e:
        logger.error(f"クラスタマッチング中にエラーが発生しました: {e}")
        logger.warning("エラーが発生したため、デフォルトのクラスタインデックス0を返します")
        return 0  # エラーが発生した場合でもデフォルト値を返す
