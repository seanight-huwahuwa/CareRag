"""
Streamlitアプリのスタイル定義
ダークモード・ライトモード対応
"""

def get_theme_css(is_dark: bool) -> str:
    """
    テーマに応じたCSSを返す
    
    Args:
        is_dark: ダークモードの場合True
        
    Returns:
        CSS文字列
    """
    theme_id = 'dark-mode' if is_dark else 'light-mode'
    
    return f"""
<style id="{theme_id}">
    /* 以前のテーマスタイルを削除 */
    #dark-mode, #light-mode {{
        display: none;
    }}
    
    :root {{
        --background-color: {'#0e1117' if is_dark else '#ffffff'};
        --text-color: {'#fafafa' if is_dark else '#262730'};
        --card-background: {'#262730' if is_dark else '#f0f2f6'};
        --border-color: {'#4a4a4a' if is_dark else '#e0e0e0'};
    }}
    
    .stApp {{
        background-color: var(--background-color);
        color: var(--text-color);
    }}
    
    /* ヘッダーバー - 背景色のみ変更、表示は維持 */
    [data-testid="stHeader"] {{
        background-color: var(--background-color);
    }}
    
    header[data-testid="stHeader"] {{
        background-color: var(--background-color) !important;
    }}
    
    /* ツールバー内の不要な要素のみ非表示 */
    [data-testid="stToolbar"] {{
        background-color: var(--background-color);
    }}
    
    /* メインメニュー（3点メニュー）を非表示 */
    #MainMenu {{
        visibility: hidden;
    }}
    
    .stMainMenu {{
        display: none;
    }}
    
    /* Deployボタンを非表示 */
    [data-testid="stStatusWidget"] {{
        display: none;
    }}
    
    /* フッター（Made with Streamlit）を非表示 */
    footer {{
        visibility: hidden;
    }}
    
    /* サイドバー */
    [data-testid="stSidebar"] {{
        background-color: {'#262730' if is_dark else '#f0f2f6'};
    }}
    
    [data-testid="stSidebar"] * {{
        color: var(--text-color) !important;
    }}
    
    [data-testid="stSidebar"] .stMarkdown {{
        color: var(--text-color) !important;
    }}
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4 {{
        color: var(--text-color) !important;
    }}
    
    /* サイドバー開閉ボタンのスタイリング */
    button[kind="header"] {{
        color: {'#ffffff !important' if is_dark else '#262730 !important'};
        background-color: {'rgba(255, 255, 255, 0.1) !important' if is_dark else 'rgba(0, 0, 0, 0.05) !important'};
        border-radius: 4px !important;
        padding: 4px 8px !important;
    }}
    
    button[kind="header"]:hover {{
        background-color: {'rgba(255, 255, 255, 0.2) !important' if is_dark else 'rgba(0, 0, 0, 0.1) !important'};
    }}
    
    button[kind="header"] svg {{
        fill: {'#ffffff !important' if is_dark else '#262730 !important'};
        stroke: {'#ffffff !important' if is_dark else '#262730 !important'};
        color: {'#ffffff !important' if is_dark else '#262730 !important'};
        opacity: 1 !important;
    }}
    
    button[kind="header"] svg path {{
        fill: {'#ffffff !important' if is_dark else '#262730 !important'};
        stroke: {'#ffffff !important' if is_dark else '#262730 !important'};
        opacity: 1 !important;
    }}
    
    button[kind="header"] svg line {{
        stroke: {'#ffffff !important' if is_dark else '#262730 !important'};
        opacity: 1 !important;
    }}
    
    button[kind="header"] svg polyline {{
        stroke: {'#ffffff !important' if is_dark else '#262730 !important'};
        opacity: 1 !important;
    }}
    
    /* ヘッダー内のサイドバーボタン */
    [data-testid="stHeader"] button[kind="header"] {{
        color: {'#ffffff !important' if is_dark else '#262730 !important'};
        background-color: {'rgba(255, 255, 255, 0.1) !important' if is_dark else 'rgba(0, 0, 0, 0.05) !important'};
        border-radius: 4px !important;
    }}
    
    [data-testid="stHeader"] button[kind="header"]:hover {{
        background-color: {'rgba(255, 255, 255, 0.2) !important' if is_dark else 'rgba(0, 0, 0, 0.1) !important'};
    }}
    
    [data-testid="stHeader"] button[kind="header"] svg {{
        fill: {'#ffffff !important' if is_dark else '#262730 !important'};
        stroke: {'#ffffff !important' if is_dark else '#262730 !important'};
        color: {'#ffffff !important' if is_dark else '#262730 !important'};
        opacity: 1 !important;
    }}
    
    [data-testid="stHeader"] button[kind="header"] svg path {{
        fill: {'#ffffff !important' if is_dark else '#262730 !important'};
        stroke: {'#ffffff !important' if is_dark else '#262730 !important'};
        opacity: 1 !important;
    }}
    
    [data-testid="stHeader"] button[kind="header"] svg line {{
        stroke: {'#ffffff !important' if is_dark else '#262730 !important'};
        opacity: 1 !important;
    }}
    
    [data-testid="stHeader"] button[kind="header"] svg polyline {{
        stroke: {'#ffffff !important' if is_dark else '#262730 !important'};
        opacity: 1 !important;
    }}
    
    [data-testid="stHeader"] button[kind="header"] svg * {{
        fill: {'#ffffff !important' if is_dark else '#262730 !important'};
        stroke: {'#ffffff !important' if is_dark else '#262730 !important'};
        opacity: 1 !important;
    }}
    
    /* サイドバーが閉じた時の開くボタン */
    [data-testid="collapsedControl"] {{
        background-color: {'rgba(255, 255, 255, 0.15) !important' if is_dark else 'rgba(0, 0, 0, 0.1) !important'};
        color: {'#ffffff !important' if is_dark else '#262730 !important'};
        border-radius: 4px !important;
    }}
    
    [data-testid="collapsedControl"]:hover {{
        background-color: {'rgba(255, 255, 255, 0.25) !important' if is_dark else 'rgba(0, 0, 0, 0.15) !important'};
    }}
    
    [data-testid="collapsedControl"] svg {{
        fill: {'#ffffff !important' if is_dark else '#262730 !important'};
        stroke: {'#ffffff !important' if is_dark else '#262730 !important'};
        opacity: 1 !important;
    }}
    
    [data-testid="collapsedControl"] svg path {{
        fill: {'#ffffff !important' if is_dark else '#262730 !important'};
        stroke: {'#ffffff !important' if is_dark else '#262730 !important'};
        opacity: 1 !important;
    }}
    
    [data-testid="collapsedControl"] svg * {{
        fill: {'#ffffff !important' if is_dark else '#262730 !important'};
        stroke: {'#ffffff !important' if is_dark else '#262730 !important'};
        opacity: 1 !important;
    }}
    
    /* テキストエリア */
    .stTextArea textarea {{
        background-color: var(--card-background);
        color: var(--text-color) !important;
        border-color: var(--border-color);
    }}
    
    .stTextArea textarea::placeholder {{
        color: {'#9e9e9e' if is_dark else '#757575'} !important;
        opacity: 1 !important;
    }}
    
    .stTextArea label {{
        color: var(--text-color) !important;
    }}
    
    /* マークダウンテキスト */
    .stMarkdown, .stMarkdown p, .stMarkdown li {{
        color: var(--text-color);
    }}
    
    /* ヘッダー */
    h1, h2, h3, h4, h5, h6 {{
        color: var(--text-color) !important;
    }}
    
    /* ボタン（プライマリ以外） */
    .stButton button:not([kind="primary"]) {{
        background-color: var(--card-background);
        color: var(--text-color);
        border: 1px solid var(--border-color);
    }}
    
    /* 検索ボタン */
    .stButton button[kind="primary"] {{
        background-color: {'#4CAF50' if is_dark else '#2196F3'};
        color: white;
        border: none;
    }}
    
    .stButton button[kind="primary"]:hover {{
        background-color: {'#45a049' if is_dark else '#1976D2'};
    }}
    
    /* ダウンロードボタン */
    .stDownloadButton button {{
        background-color: var(--card-background);
        color: var(--text-color) !important;
        border: 1px solid var(--border-color);
    }}
    
    .stDownloadButton button:hover {{
        background-color: {'#45a049' if is_dark else '#1976D2'};
        color: white !important;
    }}
    
    /* エクスパンダー */
    .st-emotion-cache-p5msec {{
        background-color: var(--card-background);
        color: var(--text-color);
    }}
    
    /* エクスパンダーの詳細スタイル */
    [data-testid="stExpander"] {{
        background-color: var(--card-background);
        border-color: var(--border-color);
    }}
    
    [data-testid="stExpander"] details {{
        background-color: var(--card-background);
    }}
    
    [data-testid="stExpander"] summary {{
        background-color: var(--card-background);
        color: var(--text-color) !important;
    }}
    
    [data-testid="stExpander"] [data-testid="stMarkdownContainer"] {{
        color: var(--text-color) !important;
    }}
    
    [data-testid="stExpander"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stExpander"] [data-testid="stMarkdownContainer"] strong {{
        color: var(--text-color) !important;
    }}
    
    [data-testid="stExpander"] div {{
        background-color: var(--card-background) !important;
        color: var(--text-color) !important;
    }}
    
    /* スピナー/ローディングメッセージ */
    .stSpinner > div {{
        border-top-color: var(--text-color) !important;
    }}
    
    .stSpinner > div > div {{
        color: var(--text-color) !important;
    }}
    
    div[data-testid="stSpinner"] {{
        color: var(--text-color) !important;
    }}
    
    div[data-testid="stSpinner"] > div {{
        color: var(--text-color) !important;
    }}
    
    /* インフォメッセージ */
    .stAlert {{
        color: var(--text-color);
    }}
    
    /* 成功メッセージ */
    .element-container .stAlert.stSuccess,
    div[data-testid="stNotificationContentSuccess"],
    .stSuccess,
    [class*="stSuccess"] {{
        background-color: {'#1e4620' if is_dark else '#d4edda'} !important;
        border-left-color: {'#4CAF50' if is_dark else '#155724'} !important;
    }}
    
    .element-container .stAlert.stSuccess *,
    div[data-testid="stNotificationContentSuccess"] *,
    .stSuccess *,
    [class*="stSuccess"] *,
    .stSuccess [data-testid="stMarkdownContainer"],
    .stSuccess [data-testid="stMarkdownContainer"] * {{
        color: {'#4CAF50' if is_dark else '#155724'} !important;
    }}
    
    /* 警告メッセージ */
    .element-container .stAlert.stWarning,
    div[data-testid="stNotificationContentWarning"],
    .stWarning,
    [class*="stWarning"] {{
        background-color: {'#4d4003' if is_dark else '#fff3cd'} !important;
        border-left-color: {'#ffeb3b' if is_dark else '#856404'} !important;
        opacity: 1 !important;
    }}
    
    .element-container .stAlert.stWarning *,
    div[data-testid="stNotificationContentWarning"] *,
    .stWarning *,
    [class*="stWarning"] *,
    .stWarning p, 
    .stWarning div, 
    .stWarning span,
    .stWarning [data-testid="stMarkdownContainer"],
    .stWarning [data-testid="stMarkdownContainer"] *,
    .stWarning [data-testid="stMarkdownContainer"] p {{
        color: {'#ffeb3b' if is_dark else '#856404'} !important;
        opacity: 1 !important;
    }}
    
    /* エラーメッセージ */
    .element-container .stAlert.stError,
    div[data-testid="stNotificationContentError"],
    .stError,
    [class*="stError"] {{
        background-color: {'#4d1414' if is_dark else '#f8d7da'} !important;
        border-left-color: {'#ff5252' if is_dark else '#721c24'} !important;
    }}
    
    .element-container .stAlert.stError *,
    div[data-testid="stNotificationContentError"] *,
    .stError *,
    [class*="stError"] *,
    .stError p, 
    .stError div, 
    .stError span,
    .stError [data-testid="stMarkdownContainer"],
    .stError [data-testid="stMarkdownContainer"] * {{
        color: {'#ff5252' if is_dark else '#721c24'} !important;
    }}
    
    /* インフォメッセージ */
    .element-container .stAlert.stInfo,
    div[data-testid="stNotificationContentInfo"],
    .stInfo,
    [class*="stInfo"] {{
        background-color: {'#0c3c55' if is_dark else '#d1ecf1'} !important;
        border-left-color: {'#03a9f4' if is_dark else '#0c5460'} !important;
    }}
    
    .element-container .stAlert.stInfo *,
    div[data-testid="stNotificationContentInfo"] *,
    .stInfo *,
    [class*="stInfo"] *,
    .stInfo p, 
    .stInfo div, 
    .stInfo span,
    .stInfo [data-testid="stMarkdownContainer"],
    .stInfo [data-testid="stMarkdownContainer"] * {{
        color: {'#03a9f4' if is_dark else '#0c5460'} !important;
    }}
</style>
"""
