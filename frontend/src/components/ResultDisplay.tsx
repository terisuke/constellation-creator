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
  };
}

const ResultDisplay: React.FC<ResultDisplayProps> = ({ result }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [error, setError] = useState<string | null>(null);
  
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
    img.crossOrigin = 'anonymous';
    
    img.onload = () => {
      // キャンバスのサイズを画像に合わせる
      canvas.width = img.width;
      canvas.height = img.height;
      
      // 画像を描画
      ctx.drawImage(img, 0, 0);
      
      // 星座ラインを描画
      if (result.constellation_lines && result.constellation_lines.length > 0) {
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.8)';
        ctx.lineWidth = 2;
        
        result.constellation_lines.forEach(line => {
          ctx.beginPath();
          ctx.moveTo(line.start.x, line.start.y);
          ctx.lineTo(line.end.x, line.end.y);
          ctx.stroke();
        });
      }
      
      // 星を描画
      if (result.stars && result.stars.length > 0) {
        ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
        result.stars.forEach(star => {
          ctx.beginPath();
          ctx.arc(star.x, star.y, 3, 0, Math.PI * 2);
          ctx.fill();
        });
      }
    };
    
    img.onerror = () => {
      setError('画像の読み込みに失敗しました');
      console.error('画像の読み込みエラー:', result.image_path);
    };
    
    img.src = result.image_path;
  }, [result]);
  
  if (!result) {
    return <div className="text-red-500">データが見つかりません</div>;
  }

  return (
    <Paper elevation={3} sx={{ p: 3, mt: 3, backgroundColor: '#1a1a1a', color: '#ffffff' }}>
      <Typography variant="h5" gutterBottom sx={{ color: '#4a90e2' }}>
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
        overflow: 'hidden'
      }}>
        <canvas 
          ref={canvasRef} 
          style={{ 
            width: '100%', 
            height: 'auto',
            display: 'block'
          }}
        />
      </Box>
      
      <Typography variant="body1" sx={{ mt: 2, whiteSpace: 'pre-line' }}>
        {result.story}
      </Typography>
    </Paper>
  );
};

export default ResultDisplay;
