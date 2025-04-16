import os
import logging
import requests
from typing import Optional
from dotenv import load_dotenv
import base64
import io
import random
from PIL import Image, ImageDraw

load_dotenv()

STABLE_DIFFUSION_API_KEY = os.getenv("STABLE_DIFFUSION_API_KEY")
if not STABLE_DIFFUSION_API_KEY:
    logging.warning("STABLE_DIFFUSION_API_KEY environment variable is not set")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_starry_image(keyword: str, output_path: Optional[str] = None) -> str:
    """
    キーワードに基づいて星空の画像を生成する
    
    Args:
        keyword: 生成のベースとなるキーワード
        output_path: 出力画像のパス（指定がない場合は自動生成）
        
    Returns:
        生成された画像のパス
    """
    try:
        if not STABLE_DIFFUSION_API_KEY or STABLE_DIFFUSION_API_KEY.startswith("sk-dummy"):
            logger.warning("ダミーのAPIキーが使用されています。サンプル画像を生成します。")
            
            
            if output_path is None:
                import uuid
                output_dir = "/tmp"
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, f"{uuid.uuid4()}_generated.jpg")
            
            img = Image.new('RGB', (800, 600), color=(0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            for _ in range(200):
                x = random.randint(0, 800)
                y = random.randint(0, 600)
                size = random.randint(1, 3)
                brightness = random.randint(150, 255)
                draw.ellipse((x-size, y-size, x+size, y+size), fill=(brightness, brightness, brightness))
            
            img.save(output_path)
            logger.info(f"ダミーの星空画像を生成しました: {output_path}")
            return output_path
            
        api_host = 'https://api.stability.ai'
        api_endpoint = f'{api_host}/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image'
        
        headers = {
            "Authorization": f"Bearer {STABLE_DIFFUSION_API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "text_prompts": [
                {
                    "text": f"beautiful starry night sky, stars, {keyword}, cosmic, high resolution, 8k",
                    "weight": 1.0
                }
            ],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30,
        }
        
        response = requests.post(api_endpoint, headers=headers, json=payload)
        
        if response.status_code != 200:
            raise ValueError(f"Stable Diffusion APIエラー: {response.text}")
            
        data = response.json()
        image_data = base64.b64decode(data["artifacts"][0]["base64"])
        
        if output_path is None:
            import uuid
            output_dir = "/tmp"
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"{uuid.uuid4()}_generated.jpg")
            
        img = Image.open(io.BytesIO(image_data))
        img.save(output_path)
        
        logger.info(f"星空画像を生成しました: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"星空画像の生成中にエラーが発生しました: {e}")
        try:
            if output_path is None:
                import uuid
                output_dir = "/tmp"
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, f"{uuid.uuid4()}_error.jpg")
            
            img = Image.new('RGB', (800, 600), color=(0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            for _ in range(100):
                x = random.randint(0, 800)
                y = random.randint(0, 600)
                size = random.randint(1, 3)
                brightness = random.randint(150, 255)
                draw.ellipse((x-size, y-size, x+size, y+size), fill=(brightness, brightness, brightness))
            
            img.save(output_path)
            logger.info(f"エラー発生時のダミー画像を生成しました: {output_path}")
            return output_path
        except Exception as inner_e:
            logger.error(f"ダミー画像の生成中にエラーが発生しました: {inner_e}")
            raise
