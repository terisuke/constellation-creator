import {
    Box,
    Button,
    Container,
    Paper,
    Typography
} from '@mui/material'
import axios from 'axios'
import { useState } from 'react'

import ImageUploader from './components/ImageUploader.tsx'
import KeywordInput from './components/KeywordInput.tsx'
import LoadingIndicator from './components/LoadingIndicator.tsx'
import ResultDisplay from './components/ResultDisplay.tsx'

function App() {
  const [keyword, setKeyword] = useState('')
  const [image, setImage] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<{
    constellation_name: string;
    story: string;
    image_path?: string;
    stars?: Array<{x: number, y: number}>;
    constellation_lines?: Array<{start: {x: number, y: number}, end: {x: number, y: number}}>;
    selected_cluster_index?: number;
  } | null>(null)

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
      console.log('Submitting constellation generation request...');
      
      const response = await axios.post('/api/generate-constellation', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      console.log('Received API response:', response.data);
      
      if (!response.data.image_path) {
        console.warn('No image path in response');
        setError('画像の生成に失敗しました');
        return;
      }
      
      if (!response.data.stars || !response.data.constellation_lines) {
        console.warn('No stars or constellation lines in response');
      }
      
      setResult({
        constellation_name: response.data.constellation_name,
        story: response.data.story,
        image_path: response.data.image_path,
        stars: response.data.stars || [],
        constellation_lines: response.data.constellation_lines || [],
        selected_cluster_index: response.data.selected_cluster_index,
      });
      
      console.log('State updated with result:', result);
      
    } catch (error) {
      console.error('Error generating constellation:', error);
      setError('星座の生成中にエラーが発生しました。もう一度お試しください。');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom align="center">
          星AI
        </Typography>
        <Typography variant="h5" component="h2" gutterBottom align="center">
          AIがあなたの「今夜だけの星座」を作ります
        </Typography>

        <Paper 
          sx={{ 
            p: 3, 
            mt: 4,
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            color: 'white'
          }}
        >
          <form onSubmit={handleSubmit}>
            {/* キーワード入力 */}
            <KeywordInput 
              value={keyword}
              onChange={setKeyword}
            />
            
            {/* 画像アップロード */}
            <ImageUploader onImageSelect={setImage} />
            
            {/* エラーメッセージ */}
            {error && (
              <Typography 
                color="error" 
                sx={{ 
                  mt: 2, 
                  p: 2, 
                  backgroundColor: 'rgba(255, 0, 0, 0.1)',
                  borderRadius: '4px'
                }}
              >
                {error}
              </Typography>
            )}

            {/* 送信ボタン */}
            <Button
              type="submit"
              variant="contained"
              fullWidth
              disabled={loading || !keyword}
              sx={{
                mt: 2,
                backgroundColor: '#4a90e2',
                '&:hover': {
                  backgroundColor: '#357abd',
                },
              }}
            >
              {loading ? '処理中...' : '星座を生成'}
            </Button>
          </form>

          {/* ローディング表示 */}
          {loading && (
            <Box sx={{ mt: 4 }}>
              <LoadingIndicator message="星座を生成中です。しばらくお待ちください..." />
            </Box>
          )}

          {/* 結果表示 */}
          {result && !loading && (
            <ResultDisplay 
              result={result}
            />
          )}
        </Paper>
      </Box>
    </Container>
  )
}

export default App                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                