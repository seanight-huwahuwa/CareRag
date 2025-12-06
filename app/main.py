"""
AIケアプラン作成支援システム
グループホーム向けケアプラン原案作成ツール
"""

import streamlit as st
import chromadb
from openai import AzureOpenAI
import os
from dotenv import load_dotenv
from pathlib import Path
from styles import get_theme_css

# 環境変数読み込み
load_dotenv()

# セッション状態初期化（ページ設定前に実行）
if 'generated_plan' not in st.session_state:
    st.session_state.generated_plan = None
if 'similar_examples' not in st.session_state:
    st.session_state.similar_examples = []
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = 'dark'
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'access_code_input' not in st.session_state:
    st.session_state.access_code_input = ""

# ページ設定
st.set_page_config(
    page_title="AIケアプラン作成支援",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="auto"
)

# テーマ適用用のカスタムCSS
is_dark = st.session_state.theme_mode == 'dark'
theme_css = get_theme_css(is_dark)

st.markdown(theme_css, unsafe_allow_html=True)
st.markdown(theme_css, unsafe_allow_html=True)

@st.cache_resource
def init_chromadb():
    """ChromaDB初期化"""
    chroma_client = chromadb.PersistentClient(
        path=str(Path(__file__).parent.parent / "chroma_db")
    )
    collection = chroma_client.get_collection(name="careplan_examples")
    return collection

@st.cache_resource
def init_azure_clients():
    """Azure OpenAIクライアント初期化"""
    endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    
    # 埋め込みクライアント
    embedding_client = AzureOpenAI(
        api_key=os.getenv('AZURE_EMBEDDING_API_KEY'),
        api_version=os.getenv('AZURE_EMBEDDING_API_VERSION', '2023-05-15'),
        azure_endpoint=endpoint
    )
    
    # GPTクライアント
    gpt_client = AzureOpenAI(
        api_key=os.getenv('AZURE_OPENAI_API_KEY'),
        api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2025-01-01-preview'),
        azure_endpoint=endpoint
    )
    
    return embedding_client, gpt_client

def search_similar_examples(collection, embedding_client, query: str, n_results: int = 5):
    """類似事例を検索"""
    # クエリをベクトル化
    response = embedding_client.embeddings.create(
        model=os.getenv('AZURE_EMBEDDING_DEPLOYMENT', 'text-embedding-3-small'),
        input=[query]
    )
    query_embedding = response.data[0].embedding
    
    # 類似検索
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    # 結果を整形
    examples = []
    for metadata in results['metadatas'][0]:
        examples.append({
            'needs': metadata.get('needs', ''),
            'long_term_goal': metadata.get('long_term_goal', ''),
            'short_term_goal': metadata.get('short_term_goal', ''),
            'service_content': metadata.get('service_content', '')
        })
    
    return examples

def generate_careplan(gpt_client, user_input: str, similar_examples: list):
    """ケアプランを生成"""
    # 類似事例をプロンプトに含める
    examples_text = "\n\n".join([
        f"【参考事例 {i+1}】\n"
        f"ニーズ: {ex['needs']}\n"
        f"長期目標: {ex['long_term_goal']}\n"
        f"短期目標: {ex['short_term_goal']}\n"
        f"サービス内容: {ex['service_content']}"
        for i, ex in enumerate(similar_examples[:3])
    ])
    
    prompt = f"""あなたはグループホームのケアプラン作成を支援する専門家です。
以下の利用者情報を基に、適切なケアプランを作成してください。

【利用者情報】
{user_input}

【参考となる類似事例】
{examples_text}

上記の参考事例を踏まえて、以下の形式でケアプランを作成してください：

1. 課題（ニーズ）
2. 長期目標
3. 短期目標
4. サービス内容

※具体的で実践可能な内容を記載してください。
※利用者の状況に合わせて柔軟に調整してください。
"""
    
    response = gpt_client.chat.completions.create(
        model=os.getenv('AZURE_GPT_DEPLOYMENT', 'dev-gpt-4o-mini'),
        messages=[
            {"role": "system", "content": "あなたはグループホームのケアプラン作成を支援する専門家です。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=2000
    )
    
    return response.choices[0].message.content

def show_access_code_page():
    """アクセスコード入力ページを表示"""
    st.markdown("""
    <style>
        .access-code-container {{
            max-width: 500px;
            margin: 100px auto;
            padding: 40px;
            background-color: {'#262730' if st.session_state.theme_mode == 'dark' else '#f0f2f6'};
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .access-code-title {{
            text-align: center;
            color: {'#fafafa' if st.session_state.theme_mode == 'dark' else '#262730'};
            margin-bottom: 30px;
        }}
    </style>
    """, unsafe_allow_html=True)
    
    # センター配置のコンテナ
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 class='access-code-title'>🔐 アクセスコード入力</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; margin-bottom: 30px;'>このシステムを使用するにはアクセスコードが必要です</p>", unsafe_allow_html=True)
        
        # アクセスコード入力
        code_input = st.text_input(
            "アクセスコード",
            type="password",
            placeholder="アクセスコードを入力してください",
            key="access_code_field"
        )
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("ログイン", use_container_width=True, type="primary"):
                access_code = os.getenv('ACCESS_CODE', '')
                if code_input == access_code:
                    st.session_state.authenticated = True
                    st.success("✅ 認証に成功しました")
                    st.rerun()
                else:
                    st.error("❌ アクセスコードが正しくありません")
        
        st.markdown("---")
        st.markdown("<p style='text-align: center; font-size: 0.9em; color: #888;'>アクセスコードをお持ちでない方は管理者にお問い合わせください</p>", unsafe_allow_html=True)

# UI構築
def main():
    # アクセスコード認証チェック
    access_code = os.getenv('ACCESS_CODE', '')
    
    # アクセスコードが設定されていて、まだ認証されていない場合
    if access_code and not st.session_state.authenticated:
        show_access_code_page()
        return
    
    st.title("🏥 AIケアプラン作成支援システム")
    st.markdown("グループホーム向けケアプラン原案作成ツール")
    
    # サイドバー表示/非表示の状態管理
    if 'sidebar_visible' not in st.session_state:
        st.session_state.sidebar_visible = True
    
    # ChromaDBとクライアント初期化
    try:
        collection = init_chromadb()
        embedding_client, gpt_client = init_azure_clients()
    except Exception as e:
        st.error(f"初期化エラー: {str(e)}")
        st.info("ChromaDBが初期化されていない場合は、まず `vectorize.py` を実行してください。")
        return
    
    # サイドバー
    with st.sidebar:
        st.header("⚙️ 設定")
        
        # ダークモード切り替え
        if 'theme_mode' not in st.session_state:
            st.session_state.theme_mode = 'dark'
        
        theme_label = "🌙 ダークモード" if st.session_state.theme_mode == 'dark' else "☀️ ライトモード"
        if st.button(theme_label, use_container_width=True):
            st.session_state.theme_mode = 'light' if st.session_state.theme_mode == 'dark' else 'dark'
            st.rerun()
        
        st.markdown("---")
        n_examples = st.slider("参考事例数", min_value=1, max_value=10, value=5)
        st.markdown("---")
        st.markdown("### 使い方")
        st.markdown("""
        1. 利用者の状況や課題を入力
        2. 「類似事例を検索」ボタンをクリック
        3. 参考事例を確認
        4. 「ケアプランを生成」ボタンをクリック
        """)
    
    # メインエリア
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 利用者情報入力")
        
        # 例文ボタン
        st.markdown("**💡 入力例（クリックで自動入力）**")
        example_col1, example_col2, example_col3 = st.columns(3)
        
        examples = [
            ("転倒予防", "85歳女性。下肢筋力の低下があり、歩行時にふらつきが見られる。転倒のリスクが高いため、安全に歩行できるようになりたいと希望している。"),
            ("認知症ケア", "78歳男性。軽度の認知症があり、物忘れが目立つ。日常生活の中で刺激を受け、認知症の進行を予防したいと考えている。"),
            ("コミュニケーション", "82歳女性。難聴があるが、他の利用者や職員とのコミュニケーションの機会を持ちたいと希望している。"),
            ("ADL維持", "75歳男性。脳梗塞後遺症により右半身に麻痺がある。リハビリを継続して、日常生活動作を維持・向上させたい。"),
            ("社会参加", "80歳女性。活動的な生活を送りたいと考えており、外出やレクリエーション活動に参加する機会を増やしたい。"),
            ("栄養改善", "77歳男性。食欲不振があり、体重が減少傾向。栄養状態を改善し、健康を維持したいと希望している。")
        ]
        
        # セッション状態から初期値取得
        if 'user_input_value' not in st.session_state:
            st.session_state.user_input_value = ""
        
        # テキストエリア
        user_input = st.text_area(
            "利用者の状況、課題、希望などを入力してください",
            value=st.session_state.user_input_value,
            height=200,
            placeholder="例: 80歳女性。軽度の認知症があり、転倒のリスクが高い。歩行時にふらつきがあり、下肢筋力の低下が見られる。本人は以前のように安全に歩きたいと希望している。"
        )
        
        # 手動入力された場合もセッション状態を更新
        if user_input != st.session_state.user_input_value:
            st.session_state.user_input_value = user_input
        
        # 例文ボタンクリック処理
        for i, (title, text) in enumerate(examples):
            col = [example_col1, example_col2, example_col3][i % 3]
            with col:
                if st.button(f"📄 {title}", key=f"example_{i}", use_container_width=True):
                    st.session_state.user_input_value = text
                    st.toast(f"✅ {title}の例文を入力しました", icon="📄")
                    st.rerun()
        
        st.markdown("---")
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("🔍 類似事例を検索", key="search_btn", type="primary", use_container_width=True):
                if user_input.strip():
                    with st.spinner("類似事例を検索中..."):
                        try:
                            examples = search_similar_examples(
                                collection, embedding_client, user_input, n_examples
                            )
                            st.session_state.similar_examples = examples
                            st.success(f"{len(examples)}件の類似事例が見つかりました")
                        except Exception as e:
                            st.error(f"検索エラー: {str(e)}")
                else:
                    st.warning("利用者情報を入力してください")
        
        with col_btn2:
            if st.button("✨ ケアプランを生成", use_container_width=True):
                if user_input.strip() and st.session_state.similar_examples:
                    with st.spinner("ケアプランを生成中..."):
                        try:
                            plan = generate_careplan(
                                gpt_client, user_input, st.session_state.similar_examples
                            )
                            st.session_state.generated_plan = plan
                            st.success("ケアプランを生成しました")
                        except Exception as e:
                            st.error(f"生成エラー: {str(e)}")
                else:
                    st.warning("まず類似事例を検索してください")
    
    with col2:
        st.header("📋 生成されたケアプラン")
        if st.session_state.generated_plan:
            st.markdown(st.session_state.generated_plan)
            
            # ダウンロードボタン
            st.download_button(
                label="📥 ケアプランをダウンロード",
                data=st.session_state.generated_plan,
                file_name="careplan.txt",
                mime="text/plain"
            )
        else:
            st.info("ケアプランを生成すると、ここに表示されます")
    
    # 類似事例表示
    if st.session_state.similar_examples:
        st.markdown("---")
        st.header("📚 参考事例")
        
        for i, example in enumerate(st.session_state.similar_examples, 1):
            with st.expander(f"参考事例 {i}: {example['needs'][:50]}..."):
                st.markdown(f"**ニーズ:** {example['needs']}")
                st.markdown(f"**長期目標:** {example['long_term_goal']}")
                st.markdown(f"**短期目標:** {example['short_term_goal']}")
                st.markdown(f"**サービス内容:** {example['service_content']}")

if __name__ == "__main__":
    main()
