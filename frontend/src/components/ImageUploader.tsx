import React, { useState } from 'react';
import { Box, Paper, Typography, Tabs, Tab } from '@mui/material';
import { useDropzone } from 'react-dropzone';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import PhotoCameraIcon from '@mui/icons-material/PhotoCamera';
import CameraCapture from './CameraCapture';

interface ImageUploaderProps {
  onImageSelect: (file: File) => void;
}

const ImageUploader: React.FC<ImageUploaderProps> = ({ onImageSelect }) => {
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
    setPreviewUrl(null);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png']
    },
    maxFiles: 1,
    onDrop: (acceptedFiles) => {
      const file = acceptedFiles[0];
      onImageSelect(file);
      
      const objectUrl = URL.createObjectURL(file);
      setPreviewUrl(objectUrl);
      
      return () => URL.revokeObjectURL(objectUrl);
    }
  });

  const handleCameraCapture = (file: File) => {
    onImageSelect(file);
  };

  return (
    <Box sx={{ mb: 3 }}>
      <Typography variant="h6" gutterBottom>
        星空の画像
      </Typography>

      {/* タブ切り替え */}
      <Tabs
        value={tabValue}
        onChange={handleTabChange}
        aria-label="画像取得方法"
        sx={{ 
          mb: 2,
          '.MuiTabs-indicator': { backgroundColor: '#4a90e2' },
          '.MuiTab-root': { color: 'rgba(255, 255, 255, 0.7)' },
          '.Mui-selected': { color: '#4a90e2 !important' }
        }}
      >
        <Tab icon={<CloudUploadIcon />} label="アップロード" />
        <Tab icon={<PhotoCameraIcon />} label="カメラで撮影" />
      </Tabs>

      {/* アップロードタブ */}
      {tabValue === 0 && (
        <Paper
          {...getRootProps()}
          sx={{
            p: 3,
            textAlign: 'center',
            backgroundColor: 'rgba(255, 255, 255, 0.1)',
            cursor: 'pointer',
            border: '2px dashed rgba(255, 255, 255, 0.3)',
            transition: 'all 0.3s ease',
            '&:hover': {
              borderColor: 'rgba(255, 255, 255, 0.5)',
              backgroundColor: 'rgba(255, 255, 255, 0.15)',
            }
          }}
        >
          <input {...getInputProps()} />
          {isDragActive ? (
            <Typography>画像をドロップしてください...</Typography>
          ) : (
            <Typography>
              クリックまたはドラッグ＆ドロップで画像をアップロード
            </Typography>
          )}
          
          {previewUrl && (
            <Box sx={{ mt: 2, position: 'relative' }}>
              <img 
                src={previewUrl} 
                alt="プレビュー" 
                style={{ 
                  maxWidth: '100%', 
                  maxHeight: '200px', 
                  borderRadius: '4px',
                  border: '1px solid rgba(255, 255, 255, 0.3)'
                }} 
              />
            </Box>
          )}
        </Paper>
      )}

      {/* カメラタブ */}
      {tabValue === 1 && (
        <CameraCapture onImageCapture={handleCameraCapture} />
      )}
    </Box>
  );
};

export default ImageUploader;
