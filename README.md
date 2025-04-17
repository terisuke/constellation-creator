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

## 主な機能

- 画像アップロードまたはカメラ撮影による星の写真の入力
- 星の検出とクラスタリング
- AIによる星座の生成（名前、物語、特徴）
- 星座線の描画と視覚化
- 複数の星座パターンの生成と選択
- 生成された星座の保存と共有

## システムアーキテクチャ

### クラウドアーキテクチャ
```mermaid
graph TB
    subgraph "Google Cloud Platform"
        CR[Cloud Run]
        CS[Cloud Storage]
        CDN[Cloud CDN]
    end
    
    subgraph "フロントエンド"
        FE[React + TypeScript]
        UI[Material-UI]
        Canvas[Canvas API]
    end
    
    subgraph "バックエンド"
        API[FastAPI]
        CV[OpenCV]
        AI[OpenAI API]
        ML[scikit-learn]
    end
    
    User((ユーザー)) --> CDN
    CDN --> CR
    CR --> CS
    CR --> API
    API --> CV
    API --> AI
    API --> ML
    FE --> API
    UI --> FE
    Canvas --> FE
```

### システム構成図
```mermaid
graph LR
    subgraph "フロントエンド"
        UI[UI Layer]
        State[State Management]
        API[API Client]
    end
    
    subgraph "バックエンド"
        EP[API Endpoints]
        Core[Core Services]
        Ext[External Services]
    end
    
    subgraph "外部サービス"
        OpenAI[OpenAI API]
        Storage[Cloud Storage]
    end
    
    UI --> State
    State --> API
    API --> EP
    EP --> Core
    Core --> Ext
    Ext --> OpenAI
    Ext --> Storage
```

## 技術スタック詳細

### フロントエンド
- React 18.2.0
- TypeScript 5.3.3
- Vite 5.0.0
- Material-UI 5.14.20
- Axios 1.6.2
- React Router DOM 6.20.1
- React Dropzone 14.2.3

### バックエンド
- Python 3.11以上
- FastAPI 0.104.1
- OpenCV 4.8.1.78
- OpenAI GPT-4 API 1.3.5
- Pillow 10.0.0
- NumPy 1.26.2
- Pydantic 2.5.2

### クラウドインフラ
- Google Cloud Run
- Google Cloud Storage
- Google Cloud CDN
- Cloud Build

## デプロイ情報

アプリケーションはGoogle Cloud Runにデプロイされています。

- 本番環境URL: https://constellation-creator-639959525777.asia-northeast1.run.app
- リージョン: asia-northeast1
- プロジェクトID: aipartner-426616

## 開発環境のセットアップ

### 必要条件
- Node.js 18以上
- Python 3.11以上
- pip
- Make

### インストール手順

1. リポジトリのクローン
```bash
git clone https://github.com/terisuke/constellation-creator.git
cd constellation-creator
```

2. Makefileを使用したセットアップ
```bash
# 開発環境の完全セットアップ（推奨）
make setup

# 依存関係のインストール
make install

# アプリケーションの実行
make run

# コードのリント
make lint

# クリーンアップ（node_modulesとvenvを削除）
make clean
```

### 手動セットアップ（Makefileを使用しない場合）

1. フロントエンドのセットアップ
```bash
cd frontend
npm install
npm run dev
```

2. バックエンドのセットアップ
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