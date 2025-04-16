import React from 'react';
import { Box, TextField, Typography } from '@mui/material';

interface KeywordInputProps {
  value: string;
  onChange: (value: string) => void;
}

const KeywordInput: React.FC<KeywordInputProps> = ({ value, onChange }) => {
  return (
    <Box sx={{ mb: 3 }}>
      <Typography 
        variant="h6" 
        gutterBottom
        sx={{ fontSize: { xs: '1.1rem', sm: '1.2rem', md: '1.25rem' } }}
      >
        キーワードを入力
      </Typography>
      <TextField
        fullWidth
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="例：希望、ドラゴン、未来..."
        variant="outlined"
        inputProps={{ 
          style: { fontSize: '1.1rem' }, // 入力フォントサイズを大きくしてタッチしやすく
          autoComplete: 'off' // モバイルでの自動補完を無効化
        }}
        sx={{ 
          '& .MuiOutlinedInput-root': {
            color: 'white',
            '& fieldset': {
              borderColor: 'rgba(255, 255, 255, 0.23)',
              borderRadius: '8px', // 角丸を強化
            },
            '&:hover fieldset': {
              borderColor: 'rgba(255, 255, 255, 0.5)',
            },
            '&.Mui-focused fieldset': {
              borderColor: '#4a90e2',
            },
            padding: { xs: '14px 14px', sm: '12px 12px', md: '10px 10px' }
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
