import { Box, Paper, Typography } from '@mui/material';
import React, { useEffect, useRef, useState } from 'react';

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
    selected_cluster_index?: number;
  };
}

const ResultDisplay: React.FC<ResultDisplayProps> = ({ result }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [error, setError] = useState<string | null>(null);
  const [imageLoaded, setImageLoaded] = useState(false);
  
  useEffect(() => {
    console.log("ResultDisplayが受信したデータ:", result);
    if (!result) {
      console.error("結果データが存在しません");
      return;
    }
    
    if (!result.image_path) {
      console.warn('画像パスが提供されていません');
      return;
    }
    
    const canvas = canvasRef.current;
    if (!canvas) {
      console.warn('キャンバスが見つかりません');
      return;
    }
    
    const ctx = canvas.getContext('2d');
    if (!ctx) {
      console.warn('キャンバスコンテキストを取得できません');
      return;
    }
    
    const img = new Image();
    
    img.onload = () => {
      // キャンバスのサイズを画像に合わせる
      canvas.width = img.width || 800;
      canvas.height = img.height || 600;
      
      // 画像を描画
      ctx.drawImage(img, 0, 0);
      
      if (result.constellation_lines && result.constellation_lines.length > 0) {
        ctx.strokeStyle = 'rgba(255, 215, 0, 0.4)'; // 黄色（薄く）
        ctx.lineWidth = 1;
        
        result.constellation_lines.forEach(line => {
          ctx.beginPath();
          ctx.moveTo(line.start.x, line.start.y);
          ctx.lineTo(line.end.x, line.end.y);
          ctx.stroke();
        });
        
        ctx.strokeStyle = 'rgba(255, 0, 0, 0.8)'; // 赤色
        ctx.lineWidth = 3; // 赤線は太く
        
        console.log("選択されたクラスタインデックス:", result.selected_cluster_index);
        
        if (result.selected_cluster_index !== undefined && result.selected_cluster_index !== null) {
          const selectedLines = result.constellation_lines.filter((_, i) => 
            Math.floor(i / 3) === result.selected_cluster_index
          );
          
          console.log("選択された線の数:", selectedLines.length);
          
          selectedLines.forEach(line => {
            ctx.beginPath();
            ctx.moveTo(line.start.x, line.start.y);
            ctx.lineTo(line.end.x, line.end.y);
            ctx.stroke();
          });
        }
      }
      
      // 星を描画
      if (result.stars && result.stars.length > 0) {
        ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
        result.stars.forEach(star => {
          ctx.beginPath();
          ctx.arc(star.x, star.y, 3, 0, Math.PI * 2);
          ctx.fill();
        });
      }
      
      setImageLoaded(true);
      setError(null);
    };
    
    img.onerror = (e) => {
      console.error('画像の読み込みエラー:', result.image_path, e);
      setError('画像の読み込みに失敗しました。別のパスで再試行します...');
      
      if (result.image_path) {
        try {
          let fallbackPath;
          
          if (result.image_path.startsWith('/static/')) {
            const fileName = result.image_path.split('/').pop();
            fallbackPath = `/api/images/${fileName}`;
          } 
          else if (result.image_path.startsWith('/api/images/')) {
            const fileName = result.image_path.split('/').pop();
            fallbackPath = `/static/images/${fileName}`;
          }
          else {
            const fileName = result.image_path.split('/').pop();
            fallbackPath = `/api/images/${fileName}`;
          }
          
          if (fallbackPath !== result.image_path) {
            console.log('フォールバックパスを試行:', fallbackPath);
            img.src = fallbackPath;
          } else {
            console.error('フォールバックパスが元のパスと同じです。再試行しません。');
          }
        } catch (err) {
          console.error('フォールバック画像の読み込みにも失敗:', err);
        }
      }
    };
    
    console.log('画像の読み込みを試行:', result.image_path);
    img.src = result.image_path;
    
  }, [result]);
  
  if (!result) {
    return <div className="text-red-500">データが見つかりません</div>;
  }

  return (
    <Paper 
      elevation={3} 
      sx={{ 
        p: { xs: 2, sm: 2, md: 3 }, 
        mt: 3, 
        backgroundColor: '#1a1a1a', 
        color: '#ffffff',
        borderRadius: '8px' // 角丸を強化
      }}
    >
      <Typography 
        variant="h5" 
        gutterBottom 
        sx={{ 
          color: '#4a90e2',
          fontSize: { xs: '1.4rem', sm: '1.5rem', md: '1.5rem' } // レスポンシブなフォントサイズ
        }}
      >
        生成された星座: {result.constellation_name}
      </Typography>
      
      {error && (
        <Typography color="error" sx={{ mb: 2 }}>
          {error}
        </Typography>
      )}
      
      <Box sx={{ 
        position: 'relative', 
        width: '100%', 
        maxWidth: '800px', 
        margin: '0 auto',
        backgroundColor: '#000',
        borderRadius: '4px',
        overflow: 'hidden',
        boxShadow: '0 4px 8px rgba(0,0,0,0.3)' // シャドウを追加
      }}>
        <canvas 
          ref={canvasRef} 
          style={{ 
            width: '100%', 
            height: 'auto',
            display: 'block',
            touchAction: 'manipulation' // タッチ操作の改善
          }}
        />
        
        {/* 画像読み込み失敗時のフォールバック表示 */}
        {!imageLoaded && result.image_path && (
          <Box sx={{ 
            p: 2, 
            textAlign: 'center', 
            color: '#aaa',
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            flexDirection: 'column'
          }}>
            <Typography variant="body2">
              画像を読み込み中...
            </Typography>
          </Box>
        )}
      </Box>
      
      <Typography 
        variant="body1" 
        sx={{ 
          mt: 2, 
          whiteSpace: 'pre-line',
          fontSize: { xs: '0.9rem', sm: '1rem', md: '1rem' }, // モバイル向けに小さめのフォント
          lineHeight: 1.6 // 読みやすさのために行間を広げる
        }}
      >
        {result.story}
      </Typography>
    </Paper>
  );
};

export default ResultDisplay;
