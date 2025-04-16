import React from 'react';
import { Box, Typography, Paper, Button } from '@mui/material';
import ShareIcon from '@mui/icons-material/Share';

interface ResultDisplayProps {
  constellationName: string;
  story: string;
  imagePath?: string;
  stars?: Array<{x: number, y: number}>;
  constellationLines?: Array<{start: {x: number, y: number}, end: {x: number, y: number}}>;
}

const ResultDisplay: React.FC<ResultDisplayProps> = ({ 
  constellationName, 
  story,
  imagePath,
  stars,
  constellationLines
}) => {
  const handleShare = () => {
  };

  const ConstellationCanvas: React.FC<{
    imagePath: string;
    stars?: Array<{x: number, y: number}>;
    constellationLines?: Array<{start: {x: number, y: number}, end: {x: number, y: number}}>;
    alt: string;
  }> = ({ imagePath, stars, constellationLines, alt }) => {
    const canvasRef = React.useRef<HTMLCanvasElement>(null);
    const [loaded, setLoaded] = React.useState(false);
    
    React.useEffect(() => {
      const img = new Image();
      img.src = imagePath;
      img.onload = () => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        
        canvas.width = img.width;
        canvas.height = img.height;
        
        const ctx = canvas.getContext('2d');
        if (!ctx) return;
        
        ctx.drawImage(img, 0, 0);
        
        if (constellationLines && constellationLines.length > 0) {
          ctx.strokeStyle = 'rgba(255, 255, 255, 0.8)';
          ctx.lineWidth = 2;
          
          constellationLines.forEach(line => {
            ctx.beginPath();
            ctx.moveTo(line.start.x, line.start.y);
            ctx.lineTo(line.end.x, line.end.y);
            ctx.stroke();
          });
        }
        
        if (stars && stars.length > 0) {
          ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
          
          stars.forEach(star => {
            ctx.beginPath();
            ctx.arc(star.x, star.y, 3, 0, Math.PI * 2);
            ctx.fill();
          });
        }
        
        setLoaded(true);
      };
    }, [imagePath, stars, constellationLines]);
    
    return (
      <>
        <canvas 
          ref={canvasRef} 
          style={{ 
            maxWidth: '100%', 
            borderRadius: '4px',
            display: loaded ? 'block' : 'none' 
          }}
        />
        {!loaded && (
          <img 
            src={imagePath} 
            alt={alt} 
            style={{ maxWidth: '100%', borderRadius: '4px' }} 
          />
        )}
      </>
    );
  };

  return (
    <Box sx={{ mt: 4 }}>
      <Paper sx={{ 
        p: 3, 
        backgroundColor: 'rgba(0, 0, 0, 0.7)',
        borderRadius: '8px',
        border: '1px solid rgba(255, 255, 255, 0.1)'
      }}>
        <Typography variant="h5" gutterBottom sx={{ color: '#4a90e2' }}>
          生成された星座: {constellationName}
        </Typography>
        
        {imagePath && (
          <Box sx={{ my: 2, textAlign: 'center', position: 'relative' }}>
            <ConstellationCanvas 
              imagePath={imagePath}
              stars={stars}
              constellationLines={constellationLines}
              alt={constellationName}
            />
          </Box>
        )}
        
        <Typography variant="body1" sx={{ whiteSpace: 'pre-line', mb: 2 }}>
          {story}
        </Typography>
        
        <Button 
          startIcon={<ShareIcon />}
          onClick={handleShare}
          variant="outlined"
          sx={{ mt: 2 }}
        >
          共有する
        </Button>
      </Paper>
    </Box>
  );
};

export default ResultDisplay;
