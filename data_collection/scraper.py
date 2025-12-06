"""
ケアプラン事例データ収集スクリプト
スクレイパー設定URLからケアプラン事例を収集する
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from pathlib import Path
from typing import List, Dict
import re
import os
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv(Path(__file__).parent.parent / '.env')

class CareplanScraper:
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv('SCRAPER_BASE_URL')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        
    def fetch_page(self, url: str) -> BeautifulSoup:
        """ページを取得してBeautifulSoupオブジェクトを返す"""
        try:
            response = self.session.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            return BeautifulSoup(response.text, 'lxml')
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def explore_site_structure(self) -> Dict:
        """サイト構造を探索"""
        print(f"Exploring {self.base_url}...")
        soup = self.fetch_page(self.base_url)
        
        if not soup:
            return {"error": "Failed to fetch main page"}
        
        # リンクを収集
        links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            text = a_tag.get_text(strip=True)
            
            # 相対URLを絶対URLに変換
            if href.startswith('/'):
                href = self.base_url + href
            elif not href.startswith('http'):
                href = self.base_url + '/' + href
                
            links.append({
                'url': href,
                'text': text
            })
        
        # ページタイトル
        title = soup.title.string if soup.title else "No title"
        
        # メインコンテンツの構造
        main_structure = {
            'title': title,
            'links_count': len(links),
            'sample_links': links[:10],  # 最初の10件
            'h1_tags': [h1.get_text(strip=True) for h1 in soup.find_all('h1')],
            'h2_tags': [h2.get_text(strip=True) for h2 in soup.find_all('h2')[:5]],
        }
        
        return main_structure
    
    def find_careplan_pages(self) -> List[str]:
        """ケアプラン事例ページのURLを検索"""
        soup = self.fetch_page(self.base_url)
        if not soup:
            return []
        
        careplan_urls = []
        
        # "ケアプラン", "事例", "認知症", "グループホーム" などのキーワードを含むリンクを探す
        keywords = ['ケアプラン', '事例', '認知症', 'グループホーム', '居宅', '施設']
        
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            text = a_tag.get_text(strip=True)
            
            # キーワードチェック
            if any(keyword in text or keyword in href for keyword in keywords):
                if href.startswith('/'):
                    href = self.base_url + href
                elif not href.startswith('http'):
                    href = self.base_url + '/' + href
                    
                if href not in careplan_urls:
                    careplan_urls.append(href)
        
        return careplan_urls
    
    def extract_careplan_data(self, url: str) -> Dict:
        """個別のケアプランページからデータを抽出"""
        soup = self.fetch_page(url)
        if not soup:
            return None
        
        data = {
            'url': url,
            'title': soup.title.string if soup.title else '',
            'needs': '',
            'long_term_goal': '',
            'short_term_goal': '',
            'service_content': '',
            'full_text': '',
            'examples': []  # 複数の事例を格納
        }
        
        # メインコンテンツを取得
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile('content|main|post'))
        
        if main_content:
            data['full_text'] = main_content.get_text(separator='\n', strip=True)
            
            # テーブルから構造化データを抽出
            tables = main_content.find_all('table')
            
            for table in tables:
                table_examples = self.extract_table_data(table, url)
                if table_examples:
                    data['examples'].extend(table_examples)
        
        return data
    
    def extract_table_data(self, table, source_url: str) -> List[Dict]:
        """テーブルから複数のケアプラン事例を抽出（行単位）"""
        examples = []
        
        rows = table.find_all('tr')
        if len(rows) < 2:  # ヘッダーとデータ行が必要
            return examples
        
        # ヘッダー行を解析
        header_row = rows[0]
        headers = [cell.get_text(strip=True) for cell in header_row.find_all(['th', 'td'])]
        
        # 各データ行を個別の事例として処理
        for row in rows[1:]:
            cells = row.find_all(['td', 'th'])
            
            if len(cells) < len(headers):
                continue
            
            example = {
                'needs': '',
                'long_term_goal': '',
                'short_term_goal': '',
                'service_content': ''
            }
            
            # 各セルをヘッダーに基づいて分類
            for i, cell in enumerate(cells):
                if i >= len(headers):
                    break
                    
                cell_text = cell.get_text(separator='\n', strip=True)
                header = headers[i]
                
                # ヘッダーに基づいて分類
                if 'ニーズ' in header or '課題' in header:
                    example['needs'] = cell_text
                elif '長期目標' in header:
                    example['long_term_goal'] = cell_text
                elif '短期目標' in header:
                    example['short_term_goal'] = cell_text
                elif 'サービス' in header or '援助' in header:
                    example['service_content'] = cell_text
            
            # 有効なデータのみ追加
            if example['needs'] or example['long_term_goal']:
                examples.append(example)
        
        return examples
    
    def save_to_json(self, data: List[Dict], filename: str):
        """データをJSONファイルに保存"""
        output_dir = Path(__file__).parent / 'raw_data'
        output_dir.mkdir(exist_ok=True)
        
        output_path = output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Saved {len(data)} items to {output_path}")
    
    def run_full_scrape(self, max_pages: int = 50, delay: int = 2):
        """完全なスクレイピングを実行"""
        print("=== Starting Full Scraping ===")
        
        # 1. サイト構造を探索
        print("\n[Step 1] Exploring site structure...")
        structure = self.explore_site_structure()
        self.save_to_json([structure], 'site_structure.json')
        
        # 2. ケアプラン関連ページを検索
        print("\n[Step 2] Finding careplan pages...")
        careplan_urls = self.find_careplan_pages()
        print(f"Found {len(careplan_urls)} potential careplan pages")
        
        # 3. 各ページからデータを抽出
        print("\n[Step 3] Extracting data from pages...")
        all_data = []
        
        for i, url in enumerate(careplan_urls[:max_pages]):
            print(f"Processing {i+1}/{min(len(careplan_urls), max_pages)}: {url}")
            
            data = self.extract_careplan_data(url)
            if data:
                all_data.append(data)
            
            # 丁寧にアクセス（サーバー負荷軽減）
            time.sleep(delay)
        
        # 4. データを保存
        print("\n[Step 4] Saving data...")
        self.save_to_json(all_data, 'careplan_data_raw.json')
        
        print(f"\n=== Scraping completed: {len(all_data)} items collected ===")
        return all_data


def main():
    """メイン実行関数"""
    scraper = CareplanScraper()
    
    # まずサイト構造を確認
    print("Exploring site structure...")
    structure = scraper.explore_site_structure()
    
    print("\n=== Site Structure ===")
    print(f"Title: {structure.get('title')}")
    print(f"Total links: {structure.get('links_count')}")
    print(f"\nH1 tags: {structure.get('h1_tags')}")
    print(f"\nSample links:")
    for link in structure.get('sample_links', []):
        print(f"  - {link['text']}: {link['url']}")
    
    # ユーザーに確認
    print("\n" + "="*50)
    response = input("Continue with full scraping? (y/n): ")
    
    if response.lower() == 'y':
        scraper.run_full_scrape(max_pages=50, delay=2)
    else:
        print("Scraping cancelled.")


if __name__ == "__main__":
    main()
