# 星AI（Constellation Creator）

AIがあなたの"今夜だけの星座"を作るWebアプリケーション

## 概要

このプロジェクトは、ユーザーがアップロードした星空の写真から、AIがその夜限りのオリジナル星座を生成するWebアプリケーションです。

### 実装済みの機能

- 星空画像のアップロード
- 星の自動検出と星座の生成
- キーワードに基づく星座名とストーリーの自動生成
- 生成された星座と検出された星のクラスタの関連付け
- 生成結果の保存と共有
- 星座の視覚化機能
  - 選択されたクラスタの強調表示
  - 星座ラインの描画最適化
  - インタラクティブな星座表示
- レスポンシブデザイン対応
  - モバイルデバイス向けのUI最適化
  - タッチ操作に適したインターフェース
  - スマートフォン向けの機能拡張
- デバイスカメラ機能
  - WebRTCを使用したカメラアクセス
  - リアルタイムプレビュー表示
  - 撮影→分析のワンクリックフロー
  - 画像品質の自動最適化

### 実装予定の機能
- 生成AIとクラスタの関連付け機能の拡張
  - より高度な特徴解析
  - 複数のクラスタ候補の提示
  - ユーザーによるクラスタ選択機能
- 星座の視覚化機能のさらなる改善
  - 3D表示オプション
  - アニメーション効果
  - インタラクティブな操作機能
- オフライン機能
  - キャッシュ戦略
  - プログレッシブWebアプリ化
- アクセシビリティ対応
- 多言語対応

## 技術スタック

### フロントエンド
- React 18.2.0
- TypeScript 5.3.3
- Vite 5.0.0
- Material-UI 5.14.20

### バックエンド
- Python 3.9以上
- FastAPI 0.104.1
- OpenCV 4.8.1.78
- OpenAI GPT-4 API

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

または、フロントエンドとバックエンドを同時に起動する場合：
```bash
cd frontend
npm run start
```

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

## プロジェクト構造

```
/
├── frontend/                     # フロントエンド（React + TypeScript + Vite）
│   ├── src/                      # ソースコード
│   │   ├── components/           # Reactコンポーネント
│   │   │   ├── ImageUploader.tsx # 画像アップロードコンポーネント
│   │   │   ├── KeywordInput.tsx  # キーワード入力コンポーネント
│   │   │   ├── ResultDisplay.tsx # 結果表示コンポーネント
│   │   │   └── LoadingIndicator.tsx # ローディング表示コンポーネント
│   │   ├── App.tsx               # メインアプリケーションコンポーネント
│   │   └── main.tsx              # エントリーポイント
│   └── ...
│
├── backend/                      # バックエンド（Python + FastAPI）
│   ├── app/                      # アプリケーションコード
│   │   ├── core/                 # コア機能
│   │   │   ├── star_detection.py # 星検出ロジック
│   │   │   ├── constellation.py  # 星座生成ロジック
│   │   │   └── image_processing.py # 画像処理
│   │   ├── services/             # 外部サービス連携
│   │   │   └── openai_service.py # OpenAI API連携
│   │   └── main.py               # アプリケーションエントリーポイント
│   ├── tests/                    # テスト
│   │   ├── test_avif_support.py  # AVIFサポートテスト
│   │   ├── test_image_processing.py # 画像処理テスト
│   │   └── test_improved_star_detection.py # 星検出テスト
│   └── ...
│
├── constellation_visualization.md # 星座の視覚化機能の実装計画
├── ROADMAP.md                    # プロジェクトロードマップ
└── ...
```

## ライセンス

MIT License                        