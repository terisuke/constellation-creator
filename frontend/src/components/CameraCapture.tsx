import React, { useRef, useState, useEffect } from 'react';
import { Box, Button, Paper, Typography, IconButton } from '@mui/material';
import PhotoCameraIcon from '@mui/icons-material/PhotoCamera';
import FlipCameraIosIcon from '@mui/icons-material/FlipCameraIos';

interface CameraCaptureProps {
  onImageCapture: (file: File) => void;
}

const CameraCapture: React.FC<CameraCaptureProps> = ({ onImageCapture }) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [isCameraAvailable, setIsCameraAvailable] = useState(false);
  const [isFrontCamera, setIsFrontCamera] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [capturedImage, setCapturedImage] = useState<string | null>(null);

  const startCamera = async (useFrontCamera = true) => {
    try {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }

      const constraints = {
        video: {
          facingMode: useFrontCamera ? 'user' : 'environment',
          width: { ideal: 1280 },
          height: { ideal: 720 }
        }
      };

      const mediaStream = await navigator.mediaDevices.getUserMedia(constraints);
      
      setStream(mediaStream);
      setIsCameraAvailable(true);
      setError(null);
      
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
    } catch (err) {
      console.error('カメラの起動に失敗しました:', err);
      setIsCameraAvailable(false);
      setError('カメラへのアクセスに失敗しました。カメラへのアクセス許可を確認してください。');
    }
  };

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
  };

  const switchCamera = () => {
    const newMode = !isFrontCamera;
    setIsFrontCamera(newMode);
    startCamera(newMode);
  };

  const captureImage = () => {
    if (!videoRef.current || !canvasRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;
    
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    const ctx = canvas.getContext('2d');
    if (ctx) {
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      
      canvas.toBlob((blob) => {
        if (blob) {
          const file = new File([blob], 'camera-capture.jpg', { type: 'image/jpeg' });
          
          const imageUrl = URL.createObjectURL(blob);
          setCapturedImage(imageUrl);
          
          onImageCapture(file);
        }
      }, 'image/jpeg', 0.9); // 品質を90%に設定して最適化
    }
  };

  const retakePhoto = () => {
    setCapturedImage(null);
    startCamera(isFrontCamera);
  };

  useEffect(() => {
    startCamera();
    
    return () => {
      stopCamera();
    };
  }, []);

  return (
    <Box sx={{ mb: 3 }}>
      <Typography variant="h6" gutterBottom>
        カメラで撮影
      </Typography>
      <Paper
        sx={{
          p: 2,
          textAlign: 'center',
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          borderRadius: '4px',
          overflow: 'hidden'
        }}
      >
        {error && (
          <Typography color="error" sx={{ mb: 2 }}>
            {error}
          </Typography>
        )}
        
        {isCameraAvailable && !capturedImage && (
          <Box sx={{ position: 'relative', width: '100%' }}>
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              style={{
                width: '100%',
                maxHeight: '300px',
                borderRadius: '4px',
                transform: isFrontCamera ? 'scaleX(-1)' : 'none',
              }}
            />
            <Box sx={{ 
              display: 'flex', 
              justifyContent: 'space-between', 
              mt: 1,
              px: 1
            }}>
              <IconButton 
                onClick={switchCamera} 
                sx={{ color: 'white' }}
                aria-label="カメラを切り替え"
              >
                <FlipCameraIosIcon />
              </IconButton>
              <Button
                onClick={captureImage}
                variant="contained"
                startIcon={<PhotoCameraIcon />}
                sx={{
                  backgroundColor: '#4a90e2',
                  '&:hover': {
                    backgroundColor: '#357abd',
                  },
                }}
              >
                撮影
              </Button>
            </Box>
          </Box>
        )}
        
        {capturedImage && (
          <Box sx={{ width: '100%' }}>
            <img
              src={capturedImage}
              alt="撮影された画像"
              style={{
                width: '100%',
                maxHeight: '300px',
                borderRadius: '4px',
                transform: isFrontCamera ? 'scaleX(-1)' : 'none',
              }}
            />
            <Button
              onClick={retakePhoto}
              variant="outlined"
              sx={{ mt: 1 }}
            >
              撮り直す
            </Button>
          </Box>
        )}
        
        {/* 非表示のキャンバス（画像キャプチャ用） */}
        <canvas
          ref={canvasRef}
          style={{ display: 'none' }}
        />
      </Paper>
    </Box>
  );
};

export default CameraCapture;
