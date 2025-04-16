import axios from 'axios';

const API_BASE_URL = 'https://constellation-creator-639959525777.asia-northeast1.run.app';

export interface ConstellationResponse {
  name: string;
  story: string;
  image_path: string;
  stars: Array<[number, number]>;
  constellation_lines: Array<[number, number]>;
  selected_cluster_index: number;
}

export const generateConstellation = async (image: File, keyword: string): Promise<ConstellationResponse> => {
  try {
    const formData = new FormData();
    formData.append('image', image);
    formData.append('keyword', keyword);

    const response = await axios.post<ConstellationResponse>(`${API_BASE_URL}/api/generate-constellation`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  } catch (error) {
    console.error('星座生成APIエラー:', error);
    throw new Error('星座の生成中にエラーが発生しました。');
  }
}; 