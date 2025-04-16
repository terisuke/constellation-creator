# 星座の視覚化機能改善実装計画

## 概要

現在の実装では、以下の問題があります：
1. AIが認識した星座が画像のどの部分から予想したものかが視覚化されていない
2. 星座の説明欄の画像表示が常に生成ミスで非表示になる
3. 生成AIで生成された星座と実際に検出された星のクラスタの間に意味的な関連付けがない

これらの問題を解決するために、以下の改善を実装します。

## 問題点

1. AIが認識した星座が画像のどの部分から予想したものかが視覚化されていない
2. 星座の説明欄の画像表示が常に生成ミスで非表示
3. 生成AIで生成された星座と実際に検出された星のクラスタの間に意味的な関連付けがない

## 解決策

1. アップされた画像にさらにレイヤーを重ねる形で星座を認識した星を白線で繋いだレイヤーを重ねて、星座の説明欄の画像表示欄で画面に表示する。

2. 生成AIとクラスタの関連付け機能を実装する：
   - 生成AIで生成された星座の特徴（形状、星の数、配置など）を解析
   - 画像から検出された星のクラスタと、生成された星座の特徴をマッチング
   - 最も適切なクラスタを選択して星座として表示
   - 選択されたクラスタを強調表示し、他のクラスタは薄く表示

## 実装計画

### バックエンド側の修正

#### 1. APIレスポンスの拡張

`backend/app/main.py`の`generate_constellation`関数を修正して、星の座標と星座ラインの情報を返すようにします。

```python
@app.post("/api/generate-constellation")
async def generate_constellation(
    keyword: str = Form(...),
    image: UploadFile = File(...)
):
    # 既存のコード...
    
    # 星の座標と星座ラインの情報を取得
    constellation_points = get_constellation_points(image_path)
    
    # 星座ラインの情報を構築
    constellation_lines = []
    for points in constellation_points:
        if len(points) >= 2:
            for i in range(len(points) - 1):
                constellation_lines.append({
                    "start": {"x": points[i][0], "y": points[i][1]},
                    "end": {"x": points[i+1][0], "y": points[i+1][1]}
                })
    
    # レスポンスに星座ラインの情報を追加
    return {
        "constellation_name": constellation_name,
        "story": story,
        "image_path": image_path,
        "stars": [{"x": point[0], "y": point[1]} for points in constellation_points for point in points],
        "constellation_lines": constellation_lines
    }
```

#### 2. 星座ライン描画機能の最適化

`backend/app/core/constellation.py`の星座ライン描画機能を最適化して、より見やすい星座ラインを生成します。

```python
def draw_constellation_lines(image_path, constellation_points, output_path=None):
    """
    星座の点を線で結んで描画する
    
    Args:
        image_path: 元画像のパス
        constellation_points: 星座の点のリスト
        output_path: 出力画像のパス（Noneの場合は元画像に上書き）
        
    Returns:
        描画された画像のパス
    """
    # 既存のコード...
    
    # 線の太さと色を調整
    line_thickness = 2
    line_color = (255, 255, 255)  # 白色
    
    # 点の大きさと色を調整
    point_radius = 3
    point_color = (255, 255, 255)  # 白色
    
    # 既存のコード...
    
    return output_path or image_path
```

#### 3. 生成AIとクラスタの関連付け機能の実装

`backend/app/core/constellation.py`に新しい関数を追加して、生成AIとクラスタの関連付けを行います。

```python
def match_constellation_with_clusters(constellation_name, constellation_story, clusters):
    """
    生成AIで生成された星座と検出された星のクラスタを関連付ける
    
    Args:
        constellation_name: 生成された星座名
        constellation_story: 生成された星座のストーリー
        clusters: 検出された星のクラスタのリスト
        
    Returns:
        最適なクラスタのインデックスと関連度スコア
    """
    # 星座名とストーリーから特徴を抽出
    features = extract_constellation_features(constellation_name, constellation_story)
    
    # 各クラスタと特徴のマッチングスコアを計算
    scores = []
    for i, cluster in enumerate(clusters):
        score = calculate_matching_score(features, cluster)
        scores.append((i, score))
    
    # スコアが最も高いクラスタを選択
    best_cluster_idx = max(scores, key=lambda x: x[1])[0]
    
    return best_cluster_idx, scores

def extract_constellation_features(name, story):
    """
    星座名とストーリーから特徴を抽出する
    
    Args:
        name: 星座名
        story: 星座のストーリー
        
    Returns:
        星座の特徴（形状、星の数、配置など）
    """
    # OpenAI APIを使用して特徴を抽出
    # または、事前定義されたパターンから特徴を抽出
    
    # 仮の実装
    return {
        "shape": "irregular",  # 形状（regular, irregular, animal, objectなど）
        "star_count": 5,       # 星の数
        "brightness": "high",  # 明るさ（high, medium, low）
        "pattern": "scattered" # パターン（scattered, dense, linearなど）
    }

def calculate_matching_score(features, cluster):
    """
    星座の特徴とクラスタのマッチングスコアを計算する
    
    Args:
        features: 星座の特徴
        cluster: 星のクラスタ
        
    Returns:
        マッチングスコア（0-1の範囲）
    """
    # 特徴とクラスタの類似度を計算
    
    # 仮の実装
    score = 0.5  # デフォルトスコア
    
    # 星の数の一致度
    star_count_match = min(len(cluster) / features["star_count"], features["star_count"] / len(cluster))
    score += star_count_match * 0.3
    
    # 明るさの一致度
    avg_brightness = sum(star["brightness"] for star in cluster) / len(cluster)
    if features["brightness"] == "high" and avg_brightness > 200:
        score += 0.2
    elif features["brightness"] == "medium" and 100 <= avg_brightness <= 200:
        score += 0.2
    elif features["brightness"] == "low" and avg_brightness < 100:
        score += 0.2
    
    # パターンの一致度（簡易実装）
    if features["pattern"] == "scattered" and len(cluster) >= 5:
        score += 0.2
    
    return min(score, 1.0)
```

### フロントエンド側の修正

#### 1. 星座ライン表示コンポーネントの実装

`frontend/src/components/ResultDisplay.tsx`を修正して、星座ラインを表示するコンポーネントを追加します。

```tsx
import React, { useEffect, useRef } from 'react';
import { Box, Typography, Paper } from '@mui/material';

interface Star {
  x: number;
  y: number;
}

interface ConstellationLine {
  start: Star;
  end: Star;
}

interface ResultDisplayProps {
  result: {
    constellation_name: string;
    story: string;
    image_path?: string;
    stars?: Star[];
    constellation_lines?: ConstellationLine[];
    selected_cluster_index?: number; // 選択されたクラスタのインデックス
  };
}

const ResultDisplay: React.FC<ResultDisplayProps> = ({ result }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  
  useEffect(() => {
    if (!result.image_path || !result.constellation_lines || !canvasRef.current) return;
    
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    // 画像を読み込む
    const img = new Image();
    img.onload = () => {
      // キャンバスのサイズを画像に合わせる
      canvas.width = img.width;
      canvas.height = img.height;
      
      // 画像を描画
      ctx.drawImage(img, 0, 0);
      
      // 星座ラインを描画
      if (result.selected_cluster_index !== undefined) {
        // 選択されたクラスタのラインを強調表示
        result.constellation_lines.forEach((line, index) => {
          const isSelected = index === result.selected_cluster_index;
          
          ctx.strokeStyle = isSelected ? 'rgba(255, 0, 0, 0.8)' : 'rgba(255, 215, 0, 0.4)';
          ctx.lineWidth = isSelected ? 3 : 1;
          
          ctx.beginPath();
          ctx.moveTo(line.start.x, line.start.y);
          ctx.lineTo(line.end.x, line.end.y);
          ctx.stroke();
        });
      } else {
        // すべてのラインを同じように表示
        ctx.strokeStyle = 'rgba(255, 215, 0, 0.8)';
        ctx.lineWidth = 2;
        
        result.constellation_lines.forEach(line => {
          ctx.beginPath();
          ctx.moveTo(line.start.x, line.start.y);
          ctx.lineTo(line.end.x, line.end.y);
          ctx.stroke();
        });
      }
      
      // 星の位置に点を描画
      ctx.fillStyle = 'white';
      result.stars?.forEach(star => {
        ctx.beginPath();
        ctx.arc(star.x, star.y, 3, 0, Math.PI * 2);
        ctx.fill();
      });
    };
    
    img.src = result.image_path;
  }, [result]);
  
  return (
    <Box sx={{ mt: 4 }}>
      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <Typography variant="h5" gutterBottom>
          {result.constellation_name}
        </Typography>
        <Typography variant="body1" paragraph>
          {result.story}
        </Typography>
      </Paper>
      
      {result.image_path && (
        <Paper elevation={3} sx={{ p: 2, textAlign: 'center' }}>
          <canvas
            ref={canvasRef}
            style={{ maxWidth: '100%', height: 'auto' }}
          />
        </Paper>
      )}
    </Box>
  );
};

export default ResultDisplay;
```

## 実装スケジュール

1. バックエンド側の修正（2週間）
   - APIレスポンスの拡張（3日）
   - 星座ライン描画機能の最適化（4日）
   - 生成AIとクラスタの関連付け機能の実装（7日）

2. フロントエンド側の修正（1週間）
   - 星座ライン表示コンポーネントの実装（3日）
   - UIの調整とテスト（4日）

3. 統合テストとデバッグ（1週間）
   - エンドツーエンドテスト（3日）
   - パフォーマンス最適化（2日）
   - バグ修正（2日）

合計: 4週間 