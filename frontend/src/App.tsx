import {
    Box,
    Button,
    CircularProgress,
    Container,
    Paper,
    TextField,
    Typography
} from '@mui/material'
import axios from 'axios'
import { useState } from 'react'
import { useDropzone } from 'react-dropzone'

function App() {
  const [keyword, setKeyword] = useState('')
  const [image, setImage] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<{
    constellation_name: string;
    story: string;
  } | null>(null)

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png']
    },
    maxFiles: 1,
    onDrop: (acceptedFiles) => {
      setImage(acceptedFiles[0])
    }
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const formData = new FormData()
      formData.append('keyword', keyword)
      if (image) {
        formData.append('image', image)
      }

      const response = await axios.post('/api/generate-constellation', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      setResult(response.data)
    } catch (error) {
      console.error('Error:', error)
      // TODO: エラーハンドリング
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
            <Box sx={{ mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                キーワードを入力
              </Typography>
              <TextField
                fullWidth
                value={keyword}
                onChange={(e) => setKeyword(e.target.value)}
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
                  },
                }}
              />
            </Box>

            <Box sx={{ mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                星空の画像をアップロード
              </Typography>
              <Paper
                {...getRootProps()}
                sx={{
                  p: 3,
                  textAlign: 'center',
                  backgroundColor: 'rgba(255, 255, 255, 0.1)',
                  cursor: 'pointer',
                  border: '2px dashed rgba(255, 255, 255, 0.3)',
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
                {image && (
                  <Typography sx={{ mt: 2 }}>
                    選択された画像: {image.name}
                  </Typography>
                )}
              </Paper>
            </Box>

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
              {loading ? <CircularProgress size={24} /> : '星座を生成'}
            </Button>
          </form>

          {result && (
            <Box sx={{ mt: 4 }}>
              <Typography variant="h5" gutterBottom>
                生成された星座: {result.constellation_name}
              </Typography>
              <Typography variant="body1" sx={{ whiteSpace: 'pre-line' }}>
                {result.story}
              </Typography>
            </Box>
          )}
        </Paper>
      </Box>
    </Container>
  )
}

export default App 