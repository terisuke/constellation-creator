import os
import logging
from typing import Dict, Any, List, Tuple
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

client = OpenAI(api_key=OPENAI_API_KEY)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_constellation_name(keyword: str, language: str = "ja") -> str:
    """
    キーワードに基づいて星座名を生成する
    
    Args:
        keyword: 生成のベースとなるキーワード
        language: 生成する言語 (jaは日本語、enは英語)
        
    Returns:
        生成された星座名
    """
    try:
        prompt = f"以下のキーワードに基づいて、新しい星座の名前を考えてください。名前は短く魅力的で、{language}で表現してください。キーワード: {keyword}"
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "あなたは創造的な星座命名AIアシスタントです。与えられたキーワードを元に、新しい星座の名前を生成します。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50
        )
        
        constellation_name = response.choices[0].message.content.strip()
        logger.info(f"星座名を生成しました: {constellation_name}")
        
        return constellation_name
    except Exception as e:
        logger.error(f"星座名の生成中にエラーが発生しました: {e}")
        return "未知の星座"

def generate_constellation_story(name: str, keyword: str, language: str = "ja") -> str:
    """
    星座名とキーワードに基づいて星座のストーリーを生成する
    
    Args:
        name: 星座の名前
        keyword: ストーリー生成のベースとなるキーワード
        language: 生成する言語 (jaは日本語、enは英語)
        
    Returns:
        生成された星座のストーリー
    """
    try:
        prompt = f"""
        以下の星座名とキーワードに基づいて、星座にまつわる物語を創作してください。
        
        星座名: {name}
        キーワード: {keyword}
        
        物語は200-300文字程度で、{language}で書いてください。
        神話的な要素や感動的なストーリーを含めると良いでしょう。
        """
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "あなたは創造的な星座物語作家AIです。与えられた星座名とキーワードを元に、魅力的な星座のストーリーを創作します。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        
        story = response.choices[0].message.content.strip()
        logger.info(f"星座ストーリーを生成しました（長さ: {len(story)}文字）")
        
        return story
    except Exception as e:
        logger.error(f"星座ストーリーの生成中にエラーが発生しました: {e}")
        return f"{name}に関する伝説は古来より語り継がれてきましたが、詳細は時間の流れとともに失われてしまいました。"
