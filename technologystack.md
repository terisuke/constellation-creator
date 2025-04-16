# 技術スタック

## フロントエンド
- React: ^18.0.0
- TypeScript: ^5.0.0
- Vite: ^5.0.0
- Material-UI: ^5.0.0

## バックエンド
- Python: ^3.9.0
- FastAPI: ^0.100.0
- OpenCV: ^4.8.0
- OpenAI GPT-4 API

## 開発ツール
- Node.js: ^18.0.0
- npm: ^10.0.0
- pip: ^23.0.0

## 外部サービス連携
- OpenAI GPT-4 API
  - 星座名生成
  - 星座ストーリー生成
- Stable Diffusion API
  - 星空画像の生成

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

# Stable Diffusion API設定
STABLE_DIFFUSION_API_KEY=your_stable_diffusion_api_key

# データベース設定
DATABASE_URL=postgresql://user:password@localhost:5432/constellation_db

# セキュリティ設定
SECRET_KEY=your_secret_key
```

## 実装規則
- フロントエンドのコンポーネントは`frontend/src/components/`に配置
- バックエンドのAPIエンドポイントは`backend/app/api/routes/`に配置
- 外部サービス連携は`backend/app/services/`に配置
- 環境変数は必ず`.env`ファイルで管理
