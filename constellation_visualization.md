# 星座の視覚化機能改善実装計画

## 概要

現在の実装では、以下の問題があります：
1. AIが認識した星座が画像のどの部分から予想したものかが視覚化されていない
2. 星座の説明欄の画像表示が常に生成ミスで非表示になる
3. 生成AIで生成された星座と実際に検出された星のクラスタの間に意味的な関連付けがない

これらの問題を解決するために、以下の改善を実装します。

## 問題点と解決策

### 1. 星座の視覚化
**問題**:
- AIが認識した星座が画像のどの部分から予想したものかが視覚化されていない
- 星座の説明欄の画像表示が常に生成ミスで非表示

**解決策**:
- アップされた画像にレイヤーを重ねて星座を表示
- 星座ラインの描画を最適化
  - 選択されたクラスタ: 赤色（rgba(255, 0, 0, 0.8)）、太さ3px
  - その他のライン: 黄色（rgba(255, 215, 0, 0.4)）、太さ1px
- インタラクティブな表示機能の追加

### 2. 生成AIとクラスタの関連付け
**問題**:
- 生成AIで生成された星座と実際に検出された星のクラスタの間に意味的な関連付けがない

**解決策**:
1. 星座の特徴解析
   - 星座名とストーリーからの特徴抽出
   - 形状、星の数、配置パターンの解析
2. クラスタとのマッチング
   - クラスタの特徴解析
   - マッチングスコアの計算
3. 最適なクラスタの選択
   - スコアに基づく最適なクラスタの選択
   - 選択されたクラスタの強調表示

## 実装計画

### バックエンド側の修正

#### 1. 星座特徴解析機能の実装
```python
def extract_constellation_features(name: str, story: str) -> dict:
    """
    星座名とストーリーから特徴を抽出する
    
    Args:
        name: 星座名
        story: 星座のストーリー
        
    Returns:
        星座の特徴（形状、星の数、配置など）
    """
    # OpenAI APIを使用して特徴を抽出
    features = {
        "shape": "irregular",  # 形状（regular, irregular, animal, objectなど）
        "star_count": 5,       # 星の数
        "brightness": "high",  # 明るさ（high, medium, low）
        "pattern": "scattered" # パターン（scattered, dense, linearなど）
    }
    return features

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
    
    # 星の数の一致度
    star_count_match = min(len(cluster) / features["star_count"], 
                          features["star_count"] / len(cluster))
    score += star_count_match * 0.3
    
    # 明るさの一致度
    avg_brightness = sum(star["brightness"] for star in cluster) / len(cluster)
    if features["brightness"] == "high" and avg_brightness > 200:
        score += 0.2
    elif features["brightness"] == "medium" and 100 <= avg_brightness <= 200:
        score += 0.2
    elif features["brightness"] == "low" and avg_brightness < 100:
        score += 0.2
    
    # パターンの一致度
    if features["pattern"] == "scattered" and len(cluster) >= 5:
        score += 0.2
    
    return min(score, 1.0)
```

#### 2. APIレスポンスの拡張
```python
@app.post("/api/generate-constellation")
async def generate_constellation(
    keyword: str = Form(...),
    image: UploadFile = File(...)
):
    # 既存のコード...
    
    # 星座の特徴を抽出
    features = extract_constellation_features(name, story)
    
    # クラスタとのマッチングスコアを計算
    scores = []
    for i, cluster in enumerate(clusters):
        score = calculate_matching_score(features, cluster)
        scores.append((i, score))
    
    # 最適なクラスタを選択
    selected_cluster_index = max(scores, key=lambda x: x[1])[0]
    
    return {
        "constellation_name": name,
        "story": story,
        "image_path": image_path,
        "stars": stars,
        "constellation_lines": constellation_lines,
        "selected_cluster_index": selected_cluster_index
    }
```

### フロントエンド側の修正

#### 1. 星座表示コンポーネントの改善
```typescript
interface ResultDisplayProps {
  result: {
    constellation_name: string;
    story: string;
    image_path?: string;
    stars?: Star[];
    constellation_lines?: ConstellationLine[];
    selected_cluster_index?: number;
  };
}

const ResultDisplay: React.FC<ResultDisplayProps> = ({ result }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  
  useEffect(() => {
    if (!canvasRef.current) return;
    
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    // 星座ラインを描画
    result.constellation_lines?.forEach((line, index) => {
      const isSelected = index === result.selected_cluster_index;
      
      ctx.strokeStyle = isSelected 
        ? 'rgba(255, 0, 0, 0.8)' 
        : 'rgba(255, 215, 0, 0.4)';
      ctx.lineWidth = isSelected ? 3 : 1;
      
      ctx.beginPath();
      ctx.moveTo(line.start.x, line.start.y);
      ctx.lineTo(line.end.x, line.end.y);
      ctx.stroke();
    });
    
    // 星を描画
    result.stars?.forEach(star => {
      ctx.fillStyle = 'white';
      ctx.beginPath();
      ctx.arc(star.x, star.y, 3, 0, Math.PI * 2);
      ctx.fill();
    });
  }, [result]);
  
  return (
    // 既存のJSX...
  );
};
```

## 実装スケジュール

1. バックエンド側の実装（2週間）
   - 星座特徴解析機能の実装（1週間）
   - APIレスポンスの拡張（3日）
   - テストの作成と実行（4日）

2. フロントエンド側の実装（1週間）
   - 星座表示コンポーネントの改善（4日）
   - UIの調整とテスト（3日）

3. 統合テストとデバッグ（1週間）
   - エンドツーエンドテスト（3日）
   - パフォーマンス最適化（2日）
   - バグ修正（2日）

合計: 4週間

## 期待される効果

1. ユーザー体験の向上
   - 生成された星座とクラスタの関連が明確に
   - より直感的な星座の視覚化
   - インタラクティブな操作性

2. システムの改善
   - より正確な星座とクラスタのマッチング
   - パフォーマンスの向上
   - コードの保守性向上 