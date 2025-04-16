import React from 'react';
import { Box, TextField, Typography } from '@mui/material';

interface KeywordInputProps {
  value: string;
  onChange: (value: string) => void;
}

const KeywordInput: React.FC<KeywordInputProps> = ({ value, onChange }) => {
  return (
    <Box sx={{ mb: 3 }}>
      <Typography variant="h6" gutterBottom>
        キーワードを入力
      </Typography>
      <TextField
        fullWidth
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="例：希望、ドラゴン、未来..."
        variant="outlined"
        sx={{ 
          '& .MuiOutlinedInput-root': {
            color: 'white',
            '& fieldset': {
              borderColor: 'rgba(255, 255, 255, 0.23)',
            },
            '&:hover fieldset': {
              borderColor: 'rgba(255, 255, 255, 0.5)',
            },
            '&.Mui-focused fieldset': {
              borderColor: '#4a90e2',
            }
          },
          '& .MuiInputBase-input': {
            '&::placeholder': {
              color: 'rgba(255, 255, 255, 0.5)',
              opacity: 1,
            }
          }
        }}
      />
    </Box>
  );
};

export default KeywordInput;
