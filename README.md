# CareRag - AIケアプラン作成支援システム

グループホーム向けケアプラン作成を支援するRAGベースのAIシステム

## プロジェクト概要

「入力は最小限、出力は専門的に」をコンセプトに、利用者の状態を入力するだけで施設サービス計画書（第2表）の原案をAIが自動作成します。

### 主な機能

- **RAG検索**: 既存の優れたケアプラン事例から類似ケースを検索
- **AI生成**: OpenAI GPT-4o-miniで専門的な文章を自動作成
- **簡単編集**: 生成された内容をブラウザ上で編集可能
- **ワンクリックコピー**: 業務ソフトやExcelへ簡単に貼り付け

## 技術スタック

- **Frontend/Backend**: Python 3.10 + Streamlit
- **LLM**: OpenAI API (GPT-4o-mini)
- **Vector DB**: ChromaDB
- **Embedding**: OpenAI text-embedding-3-small
- **Hosting**: Streamlit Community Cloud

## プロジェクト構造

```
CareRag/
├── data_collection/          # データ収集・前処理
│   ├── scraper.py           # Webスクレイピング
│   ├── raw_data/            # 生データ
│   │   └── facility_careplan_examples.json
│   └── processed_data/      # 処理済みデータ
│       └── individual_examples.json
├── chroma_db/               # ベクトルデータベース
│   └── chroma.sqlite3       # ChromaDB
├── app/                     # Streamlitアプリ
│   ├── main.py             # メインアプリ
│   └── styles.py           # UIスタイル定義
├── vectorize.py             # ベクトル化スクリプト
├── .env                     # 環境変数（API KEY等）
├── .env.example             # 環境変数サンプル
├── requirements.txt         # 依存パッケージ
├── DEPLOYMENT.md            # デプロイメント手順
├── DevelopmentPlan.md       # 開発計画
└── README.md               # このファイル
```

## セットアップ

### 1. 環境構築

```bash
# Conda環境作成
conda create -n carerag python=3.10
conda activate carerag

# パッケージインストール
pip install -r requirements.txt
```

### 2. 環境変数設定

`.env` ファイルを作成し、OpenAI API Keyを設定:

```
OPENAI_API_KEY=your_api_key_here
```

### 3. データ収集（Phase 1）

```bash
cd data_collection
python scraper.py          # ケアプラン事例を収集
```

### 4. ベクトルDB構築（Phase 1）

```bash
python vectorize.py        # ChromaDBにデータを格納
```

### 5. アプリ起動（Phase 2）

```bash
streamlit run app/main.py --server.port 8501
```

## 開発ロードマップ

### ✅ Phase 1: データセットの構築
- [x] データ収集スクリプト作成
- [x] データクリーニング・構造化
- [x] ベクトルデータベース構築

### 🔄 Phase 2: プロトタイプ開発
- [x] Streamlit基本UI実装
- [x] RAG検索機能実装
- [x] GPT-4o-mini統合
- [x] プロンプトエンジニアリング

### 📋 Phase 3: デプロイとテスト
- [ ] Streamlit Community Cloudデプロイ
- [ ] ユーザーテスト実施
- [ ] フィードバック反映

### 🚀 Phase 4: ブログ公開
- [ ] 利用規約・免責事項作成
- [ ] ブログ記事作成
- [ ] 一般公開

## データ収集実績

- **構造化データ**: 298件のケアプラン事例
- **データ項目**: ニーズ、長期目標、短期目標、サービス内容

### 収集データ構造

```json
{
  "needs": "生活全般の解決すべき課題",
  "long_term_goal": "長期目標（1年）",
  "short_term_goal": "短期目標（3ヶ月）",
  "service_content": "援助内容",
}
```

## 免責事項

⚠️ **重要な注意事項**

- 本システムが出力するプランは「原案」です
- 最終決定は必ず有資格者（計画作成担当者）が行ってください
- 入力欄には個人情報（実名等）を入力しないでください
- 参照元データは内部処理のみに使用しています

## ライセンス

個人利用・学習目的での使用を想定しています。
商用利用の場合は別途ご相談ください。

## 開発者

- 開発環境: Python 3.10.19, Ubuntu Linux
- GPU: RTX 3090 (将来的にローカルLLM対応予定)

---

**作成日**: 2025年12月5日
**最終更新**: 2025年12月5日
