export const generateConstellation = async (
  keyword: string,
  image: File
): Promise<ConstellationResponse> => {
  try {
    console.log("APIリクエスト開始 - パラメータ:", { keyword, image });

    const formData = new FormData();
    formData.append("keyword", keyword);
    formData.append("image", image);

    const response = await fetch("/api/generate-constellation", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      console.error("APIエラー:", response.status, response.statusText);
      throw new Error(`APIエラー: ${response.status}`);
    }

    const data = await response.json();
    console.log("API応答データ:", data);
    return data;
  } catch (error) {
    console.error("API呼び出し中にエラーが発生:", error);
    throw error;
  }
}; 