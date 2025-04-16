import React from 'react';
import { Box, Typography, Paper, Button } from '@mui/material';
import ShareIcon from '@mui/icons-material/Share';

interface ResultDisplayProps {
  constellationName: string;
  story: string;
  imagePath?: string;
}

const ResultDisplay: React.FC<ResultDisplayProps> = ({ 
  constellationName, 
  story,
  imagePath 
}) => {
  const handleShare = () => {
    console.log('共有機能は将来的に実装予定です');
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
          <Box sx={{ my: 2, textAlign: 'center' }}>
            <img 
              src={imagePath} 
              alt={constellationName} 
              style={{ maxWidth: '100%', borderRadius: '4px' }} 
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
