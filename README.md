# 星AI（Constellation Creator）

AIがあなたの"今夜だけの星座"を作るWebアプリケーション

## 概要

このプロジェクトは、ユーザーがアップロードした星空の写真から、AIがその夜限りのオリジナル星座を生成するWebアプリケーションです。

### 主な機能

- 星空画像のアップロード
- 星の自動検出と星座の生成
- キーワードに基づく星座名とストーリーの自動生成
- 生成結果の保存と共有

## 技術スタック

### フロントエンド
- React
- TypeScript
- Material-UI

### バックエンド
- Python
- FastAPI
- OpenCV
- OpenAI GPT-4

## 開発環境のセットアップ

### 必要条件
- Node.js 18以上
- Python 3.9以上
- pip

### インストール手順

1. リポジトリのクローン
```bash
git clone [repository-url]
cd constellation-creator
```

2. フロントエンドのセットアップ
```bash
cd frontend
npm install
npm run dev
```

3. バックエンドのセットアップ
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

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

## ライセンス

MIT License  