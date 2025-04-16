# 星座の視覚化機能改善実装計画

## 概要

現在の実装では、AIが認識した星座が画像のどの部分から予想したものかが視覚化されていない問題と、星座の説明欄の画像表示が常に生成ミスで非表示になる問題があります。これらの問題を解決するために、以下の改善を実装します。

## 問題点

1. AIが認識した星座が画像のどの部分から予想したものかが視覚化されていない
2. 星座の説明のすぐ上に画像アイコンが常に表示されているが、常に生成ミスで非表示

## 解決策

アップされた画像にさらにレイヤーを重ねる形で星座を認識した星を白線で繋いだレイヤーを重ねて、星座の説明欄の画像表示欄で画面に表示する。

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
      ctx.strokeStyle = 'white';
      ctx.lineWidth = 2;
      
      result.constellation_lines.forEach(line => {
        ctx.beginPath();
        ctx.moveTo(line.start.x, line.start.y);
        ctx.lineTo(line.end.x, line.end.y);
        ctx.stroke();
      });
      
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
    <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
      <Typography variant="h5" gutterBottom>
        あなたの星座: {result.constellation_name}
      </Typography>
      
      {result.image_path && (
        <Box sx={{ position: 'relative', width: '100%', maxWidth: '800px', margin: '0 auto' }}>
          <canvas 
            ref={canvasRef} 
            style={{ width: '100%', height: 'auto' }}
          />
        </Box>
      )}
      
      <Typography variant="body1" sx={{ mt: 2 }}>
        {result.story}
      </Typography>
    </Paper>
  );
};

export default ResultDisplay;
```

#### 2. 星座の説明欄の画像表示修正

`frontend/src/App.tsx`の`handleSubmit`関数を修正して、APIレスポンスから星座ライン情報を取得し、`ResultDisplay`コンポーネントに渡すようにします。

```tsx
const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  setLoading(true);
  setError(null);
  
  if (!image) {
    setError('画像をアップロードしてください');
    setLoading(false);
    return;
  }
  
  if (!keyword) {
    setError('キーワードを入力してください');
    setLoading(false);
    return;
  }
  
  const formData = new FormData();
  formData.append('image', image);
  formData.append('keyword', keyword);
  
  try {
    const response = await axios.post('/api/generate-constellation', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    setResult({
      constellation_name: response.data.constellation_name,
      story: response.data.story,
      image_path: response.data.image_path,
      stars: response.data.stars,
      constellation_lines: response.data.constellation_lines,
    });
  } catch (error) {
    console.error('Error generating constellation:', error);
    setError('星座の生成中にエラーが発生しました。もう一度お試しください。');
  } finally {
    setLoading(false);
  }
};
```

## 期待される効果

1. ユーザーはAIが認識した星座が画像のどの部分から予想したものかを視覚的に確認できるようになります。
2. 星座の説明欄に正しく画像が表示されるようになります。
3. ユーザー体験が向上し、アプリケーションの価値が高まります。

## 実装スケジュール

1. バックエンド側の修正（1日）
   - APIレスポンスの拡張
   - 星座ライン描画機能の最適化

2. フロントエンド側の修正（1日）
   - 星座ライン表示コンポーネントの実装
   - 星座の説明欄の画像表示修正

3. テストとデバッグ（1日）
   - 機能テスト
   - エッジケースの確認
   - パフォーマンス最適化

合計: 3日間 