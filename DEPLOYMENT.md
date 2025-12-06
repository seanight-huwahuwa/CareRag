# Streamlit Community Cloud デプロイ用のシークレット設定

Streamlit Community Cloudにデプロイする際は、以下の環境変数を設定してください。

## 設定方法

1. Streamlit Community Cloudのダッシュボードで、アプリの「Settings」を開く
2. 「Secrets」タブを選択
3. 以下の内容をTOML形式で入力

```toml
# Azure OpenAI API設定
AZURE_OPENAI_API_KEY = "your_gpt_api_key_here"
AZURE_EMBEDDING_API_KEY = "your_embedding_api_key_here"
AZURE_OPENAI_ENDPOINT = "https://your-resource.cognitiveservices.azure.com/"
AZURE_OPENAI_API_VERSION = "2025-01-01-preview"
AZURE_EMBEDDING_API_VERSION = "2023-05-15"
AZURE_EMBEDDING_DEPLOYMENT = "text-embedding-3-small"
AZURE_GPT_DEPLOYMENT = "gpt-4o-mini"

# アクセスコード（システム利用のための認証コード）
ACCESS_CODE = "your_secure_access_code_here"
```

## 注意事項

- 実際のAPIキーとエンドポイントに置き換えてください
- シークレットは暗号化されて保存されます
- `.env`ファイルの内容はGitHubにプッシュしないでください
