import React from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';

interface LoadingIndicatorProps {
  message?: string;
  progress?: number;
}

const LoadingIndicator: React.FC<LoadingIndicatorProps> = ({ 
  message = '処理中...',
  progress 
}) => {
  return (
    <Box 
      sx={{ 
        display: 'flex', 
        flexDirection: 'column',
        alignItems: 'center', 
        justifyContent: 'center',
        p: 3
      }}
    >
      <Box sx={{ position: 'relative', display: 'inline-flex' }}>
        <CircularProgress 
          size={60} 
          thickness={4} 
          variant={progress !== undefined ? 'determinate' : 'indeterminate'} 
          value={progress} 
          sx={{ color: '#4a90e2' }}
        />
        {progress !== undefined && (
          <Box
            sx={{
              top: 0,
              left: 0,
              bottom: 0,
              right: 0,
              position: 'absolute',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <Typography variant="caption" sx={{ color: 'white' }}>
              {`${Math.round(progress)}%`}
            </Typography>
          </Box>
        )}
      </Box>
      <Typography variant="body2" sx={{ mt: 2, color: 'white' }}>
        {message}
      </Typography>
    </Box>
  );
};

export default LoadingIndicator;
