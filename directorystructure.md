# ディレクトリ構成

以下のディレクトリ構造に従って実装を行ってください：

```
/
├── frontend/                     # フロントエンド（React + TypeScript + Vite）
│   ├── public/                   # 静的ファイル
│   ├── src/                      # ソースコード
│   │   ├── components/           # Reactコンポーネント
│   │   │   ├── ImageUploader.tsx # 画像アップロードコンポーネント
│   │   │   ├── KeywordInput.tsx  # キーワード入力コンポーネント
│   │   │   ├── ResultDisplay.tsx # 結果表示コンポーネント
│   │   │   └── LoadingIndicator.tsx # ローディング表示コンポーネント
│   │   ├── services/             # APIサービス
│   │   │   └── api.ts            # バックエンドAPIとの通信
│   │   ├── types/                # 型定義
│   │   │   └── index.ts          # 共通型定義
│   │   ├── utils/                # ユーティリティ関数
│   │   ├── App.tsx               # メインアプリケーションコンポーネント
│   │   └── main.tsx              # エントリーポイント
│   ├── index.html                # HTMLテンプレート
│   ├── package.json              # 依存関係
│   ├── tsconfig.json             # TypeScript設定
│   └── vite.config.ts            # Vite設定
│
├── backend/                      # バックエンド（Python + FastAPI）
│   ├── app/                      # アプリケーションコード
│   │   ├── api/                  # APIエンドポイント
│   │   │   └── routes/           # ルート定義
│   │   ├── core/                 # コア機能
│   │   │   ├── star_detection.py # 星検出ロジック
│   │   │   ├── constellation.py  # 星座生成ロジック
│   │   │   └── image_processing.py # 画像処理
│   │   ├── services/             # 外部サービス連携
│   │   │   ├── openai_service.py # OpenAI API連携
│   │   │   └── stable_diffusion.py # Stable Diffusion API連携
│   │   ├── utils/                # ユーティリティ
│   │   └── main.py               # アプリケーションエントリーポイント
│   ├── tests/                    # テスト
│   ├── .env                      # 環境変数
│   └── requirements.txt          # 依存関係
│
├── .git/                         # Gitリポジトリ
├── .gitignore                    # Git除外設定
├── README.md                     # プロジェクト説明
└── ROADMAP.md                    # プロジェクトロードマップ
```

### 配置ルール
- フロントエンドコンポーネント → `frontend/src/components/`
- バックエンドAPIエンドポイント → `backend/app/api/routes/`
- 共通処理 → `frontend/src/utils/` または `backend/app/utils/`
- 外部サービス連携 → `backend/app/services/`