# 技術スタック

## フロントエンド
- React: 18.2.0
- TypeScript: 5.3.3
- Vite: 5.0.0
- Material-UI: 5.14.20
- Axios: 1.6.2
- React Router DOM: 6.20.1
- React Dropzone: 14.2.3

## バックエンド
- Python: 3.9以上
- FastAPI: 0.104.1
- OpenCV: 4.8.1.78
- OpenAI GPT-4 API: 1.3.5
- Pillow: 10.1.0
- NumPy: 1.26.2
- Pydantic: 2.5.2

## 開発ツール
- Node.js: 18以上
- npm: 10.0.0以上
- pip: 23.0.0以上

## 外部サービス連携
- OpenAI GPT-4 API
  - 星座名生成
  - 星座ストーリー生成

## 画像処理機能
- OpenCV
  - 星の検出
  - 画像の前処理
  - 星座ラインの描画
- Pillow
  - 画像フォーマット変換
  - 画像の最適化

## 環境変数
バックエンドの`.env`ファイルに以下の環境変数を設定してください：
```
# OpenAI API設定
OPENAI_API_KEY=your_openai_api_key

# データベース設定
DATABASE_URL=postgresql://user:password@localhost:5432/constellation_db

# セキュリティ設定
SECRET_KEY=your_secret_key
```

## 実装規則
- フロントエンドのコンポーネントは`frontend/src/components/`に配置
- バックエンドのAPIエンドポイントは`backend/app/main.py`に配置
- 外部サービス連携は`backend/app/services/`に配置
- コア機能は`backend/app/core/`に配置
- 環境変数は必ず`.env`ファイルで管理
