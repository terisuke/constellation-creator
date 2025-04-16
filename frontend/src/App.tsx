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
import ResultDisplay from './components/ResultDisplay.tsx'
import LoadingIndicator from './components/LoadingIndicator.tsx'

function App() {
  const [keyword, setKeyword] = useState('')
  const [image, setImage] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<{
    constellation_name: string;
    story: string;
    image_path?: string;
  } | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    if (!image) {
      setError('星座を生成するには画像をアップロードしてください。')
      setLoading(false)
      return
    }

    try {
      let formData = new FormData()
      formData.append('keyword', keyword)
      formData.append('image', image)
      
      const response = await axios.post('/api/generate-constellation', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      setResult(response.data)
    } catch (error) {
      console.error('Error:', error)
      setError('星座の生成中にエラーが発生しました。もう一度お試しください。')
    } finally {
      setLoading(false)
    }
  }

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
              constellationName={result.constellation_name}
              story={result.story}
              imagePath={result.image_path}
            />
          )}
        </Paper>
      </Box>
    </Container>
  )
}

export default App                          