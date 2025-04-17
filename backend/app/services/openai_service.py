import os
import logging
from typing import Dict, Any, List, Tuple
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logging.warning("OPENAI_API_KEY environment variable is not set")

if OPENAI_API_KEY and OPENAI_API_KEY.startswith("sk-dummy"):
    logging.warning("ダミーのOpenAI APIキーが使用されています。モックレスポンスを返します。")

client = None
if OPENAI_API_KEY:
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
    if not OPENAI_API_KEY or not client or (OPENAI_API_KEY and OPENAI_API_KEY.startswith("sk-dummy")):
        logger.warning("APIキーが設定されていないか、ダミーのAPIキーが使用されています。モック星座名を返します。")
        
        mock_names = {
            "希望": "光明の星座",
            "愛": "心結びの星座",
            "勇気": "獅子心の星座",
            "自由": "風翔の星座",
            "平和": "静寂の星座",
            "夢": "夢幻の星座",
            "未来": "時の扉の星座",
            "海": "深海の星座",
            "空": "蒼穹の星座",
            "火": "炎獅子の星座",
            "水": "流水の星座",
            "風": "疾風の星座",
            "地": "大地の星座",
            "光": "光輝の星座",
            "闇": "暗影の星座"
        }
        
        for key, name in mock_names.items():
            if key in keyword:
                return name
        
        return f"{keyword}の星座"
    
    try:
        prompt = f"以下のキーワードに基づいて、新しい星座の名前を考えてください。名前は短く魅力的で、{language}で表現してください。キーワード: {keyword}"
        
        response = client.chat.completions.create(
            model="gpt-4.1-2025-04-14",
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
    if not OPENAI_API_KEY or not client or (OPENAI_API_KEY and OPENAI_API_KEY.startswith("sk-dummy")):
        logger.warning("APIキーが設定されていないか、ダミーのAPIキーが使用されています。モック星座ストーリーを返します。")
        
        mock_stories = {
            "希望": f"古来より、{name}は希望の象徴とされてきました。暗闇の中で最も明るく輝くその星々は、困難な時代を生きる人々に勇気を与えてきたと言われています。伝説によれば、かつて大きな災害に見舞われた村があり、人々は絶望の淵にありました。しかしある夜、空に現れた{name}の光が人々の心に希望を灯し、村は再建への道を歩み始めたといいます。今でも、人生の岐路に立つ者が{name}を見上げると、新たな道が開けると信じられています。",
            "愛": f"{name}は、永遠の愛を象徴する星座です。二つの明るい星が中心にあり、それらは離れていても常に引き合う運命にあるとされています。伝説では、身分違いの恋に落ちた二人の若者が、別々の道を歩むことを余儀なくされましたが、神々は彼らの純粋な愛に感動し、死後に星となって永遠に寄り添えるようにしたと言われています。今でも、{name}が最も輝く夜に愛を誓うと、その絆は永遠に続くと信じられています。",
            "勇気": f"{name}は、古代の勇者の姿を映した星座です。伝説によれば、恐ろしい魔物が世界を脅かしていた時代、一人の若者が立ち上がり、自らの命を顧みず戦いに挑んだといいます。長く苦しい戦いの末、若者は魔物を倒しましたが、自身も深い傷を負いました。神々は若者の勇気を称え、その姿を星座として空に描きました。以来、{name}は困難に立ち向かう全ての人の守護星となり、勇気と決断の象徴として崇められています。"
        }
        
        for key, story in mock_stories.items():
            if key in keyword:
                return story
        
        return f"{name}に関する伝説は古来より語り継がれてきました。星々の配置は、{keyword}にまつわる物語を表しているとされています。詳細は時間の流れとともに変化してきましたが、今でも多くの人々がこの星座に特別な意味を見出し、夜空を見上げては思いを馳せています。"
    
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

def extract_constellation_features(name: str, story: str) -> dict:
    """
    星座名とストーリーから特徴を抽出する
    
    Args:
        name: 星座名
        story: 星座のストーリー
        
    Returns:
        星座の特徴（形状、星の数、配置など）
    """
    if not OPENAI_API_KEY or not client or (OPENAI_API_KEY and OPENAI_API_KEY.startswith("sk-dummy")):
        logger.warning("APIキーが設定されていないか、ダミーのAPIキーが使用されています。モック特徴を返します。")
        return {
            "shape": "irregular",
            "star_count": 5,
            "brightness": "high",
            "pattern": "scattered"
        }
    
    try:
        prompt = f"""
        以下の星座名とストーリーから、星座の特徴を抽出してください。
        
        星座名: {name}
        ストーリー: {story}
        
        以下の形式で特徴を抽出してください：
        - 形状（shape）: regular, irregular, animal, object など
        - 星の数（star_count）: おおよその数（5-15の数値）
        - 明るさ（brightness）: high, medium, low のいずれか
        - パターン（pattern）: scattered, dense, linear のいずれか
        """
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "あなたは星座の特徴を抽出するAIアシスタントです。与えられた星座名とストーリーから、星座の形状、星の数、明るさ、パターンなどの特徴を抽出します。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )
        
        feature_text = response.choices[0].message.content.strip()
        logger.info(f"抽出された特徴テキスト: {feature_text}")
        
        features = {
            "shape": "irregular",
            "star_count": 5,
            "brightness": "high",
            "pattern": "scattered"
        }
        
        if "regular" in feature_text.lower():
            features["shape"] = "regular"
        elif "animal" in feature_text.lower():
            features["shape"] = "animal"
        elif "object" in feature_text.lower():
            features["shape"] = "object"
            
        if "linear" in feature_text.lower():
            features["pattern"] = "linear"
        elif "dense" in feature_text.lower():
            features["pattern"] = "dense"
            
        if "低い" in feature_text.lower() or "low" in feature_text.lower():
            features["brightness"] = "low"
        elif "中程度" in feature_text.lower() or "medium" in feature_text.lower():
            features["brightness"] = "medium"
            
        import re
        numbers = re.findall(r'\d+', feature_text)
        if numbers:
            for num in numbers:
                n = int(num)
                if 3 <= n <= 20:  # 星の数として妥当な範囲
                    features["star_count"] = n
                    break
                    
        logger.info(f"解析された特徴: {features}")
        return features
    except Exception as e:
        logger.error(f"星座特徴の抽出中にエラーが発生しました: {e}")
        return {
            "shape": "irregular",
            "star_count": 5,
            "brightness": "high",
            "pattern": "scattered"
        }
