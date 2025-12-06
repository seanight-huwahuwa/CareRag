"""
ケアプラン事例をChromaDBにベクトル化して保存
"""

import json
import chromadb
from chromadb.config import Settings
from pathlib import Path
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()

def load_careplan_data(json_file: str) -> list:
    """JSONファイルからケアプラン事例を読み込み"""
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_embedding_text(example: dict) -> str:
    """事例から埋め込み用のテキストを作成"""
    parts = []
    
    if example.get('needs'):
        parts.append(f"ニーズ: {example['needs']}")
    if example.get('long_term_goal'):
        parts.append(f"長期目標: {example['long_term_goal']}")
    if example.get('short_term_goal'):
        parts.append(f"短期目標: {example['short_term_goal']}")
    if example.get('service_content'):
        parts.append(f"サービス内容: {example['service_content']}")
    
    return '\n'.join(parts)

def vectorize_and_store(data_file: str, collection_name: str = "careplan_examples"):
    """ケアプラン事例をベクトル化してChromaDBに保存"""
    
    # Azure OpenAI設定確認
    embedding_api_key = os.getenv('AZURE_EMBEDDING_API_KEY') or os.getenv('AZURE_OPENAI_API_KEY')
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    api_version = os.getenv('AZURE_EMBEDDING_API_VERSION', '2023-05-15')
    embedding_deployment = os.getenv('AZURE_EMBEDDING_DEPLOYMENT', 'text-embedding-3-small')
    
    if not embedding_api_key or not endpoint:
        raise ValueError("AZURE_EMBEDDING_API_KEY (または AZURE_OPENAI_API_KEY) と AZURE_OPENAI_ENDPOINT 環境変数が必要です")
    
    client = AzureOpenAI(
        api_key=embedding_api_key,
        api_version=api_version,
        azure_endpoint=endpoint
    )
    
    # ChromaDBクライアント初期化
    chroma_client = chromadb.PersistentClient(
        path=str(Path(__file__).parent / "chroma_db")
    )
    
    # 既存のコレクションがあれば削除
    try:
        chroma_client.delete_collection(name=collection_name)
        print(f"既存のコレクション '{collection_name}' を削除しました")
    except:
        pass
    
    # 新しいコレクション作成
    collection = chroma_client.create_collection(
        name=collection_name,
        metadata={"description": "施設ケアプラン事例"}
    )
    
    # データ読み込み
    examples = load_careplan_data(data_file)
    print(f"\n読み込んだ事例数: {len(examples)}")
    
    # バッチ処理でベクトル化
    batch_size = 100
    total_batches = (len(examples) + batch_size - 1) // batch_size
    
    for batch_idx in range(total_batches):
        start_idx = batch_idx * batch_size
        end_idx = min(start_idx + batch_size, len(examples))
        batch = examples[start_idx:end_idx]
        
        print(f"\nバッチ {batch_idx + 1}/{total_batches} を処理中... ({start_idx + 1}-{end_idx})")
        
        # 埋め込み用テキスト作成
        texts = [create_embedding_text(ex) for ex in batch]
        
        # OpenAI Embeddings API でベクトル化
        print("  Azure OpenAI APIで埋め込みベクトルを生成中...")
        response = client.embeddings.create(
            model=embedding_deployment,
            input=texts
        )
        
        embeddings = [item.embedding for item in response.data]
        
        # ChromaDBに追加
        ids = [f"example_{start_idx + i}" for i in range(len(batch))]
        metadatas = [
            {
                'needs': ex.get('needs', ''),
                'long_term_goal': ex.get('long_term_goal', ''),
                'short_term_goal': ex.get('short_term_goal', ''),
                'service_content': ex.get('service_content', '')
            }
            for ex in batch
        ]
        
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )
        
        print(f"  {len(batch)}件をChromaDBに追加しました")
    
    # 統計情報
    total_count = collection.count()
    print(f"\n{'='*50}")
    print(f"ベクトル化完了!")
    print(f"総事例数: {total_count}")
    print(f"コレクション名: {collection_name}")
    print(f"保存先: {Path(__file__).parent / 'chroma_db'}")
    print(f"{'='*50}\n")
    
    return collection

def test_search(collection, query: str, n_results: int = 3):
    """検索テスト"""
    print(f"\n検索クエリ: '{query}'")
    print(f"{'='*50}")
    
    # Azure OpenAI APIでクエリをベクトル化
    embedding_api_key = os.getenv('AZURE_EMBEDDING_API_KEY') or os.getenv('AZURE_OPENAI_API_KEY')
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    api_version = os.getenv('AZURE_EMBEDDING_API_VERSION', '2023-05-15')
    embedding_deployment = os.getenv('AZURE_EMBEDDING_DEPLOYMENT', 'text-embedding-3-small')
    
    client = AzureOpenAI(
        api_key=embedding_api_key,
        api_version=api_version,
        azure_endpoint=endpoint
    )
    
    response = client.embeddings.create(
        model=embedding_deployment,
        input=[query]
    )
    query_embedding = response.data[0].embedding
    
    # 類似検索
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    # 結果表示
    for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0]), 1):
        print(f"\n【結果 {i}】")
        print(f"ニーズ: {metadata['needs']}")
        print(f"長期目標: {metadata['long_term_goal']}")
        print(f"短期目標: {metadata['short_term_goal']}")
        print(f"サービス内容: {metadata['service_content'][:100]}...")

if __name__ == "__main__":
    # データファイルパス
    data_file = Path(__file__).parent / "data_collection/processed_data/individual_examples.json"
    
    # ベクトル化実行
    collection = vectorize_and_store(str(data_file))
    
    # 検索テスト
    test_queries = [
        "転倒を防止したい",
        "認知症の進行を予防したい",
        "コミュニケーション能力を向上させたい"
    ]
    
    for query in test_queries:
        test_search(collection, query, n_results=3)
        print()
