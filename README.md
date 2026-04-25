#AI Document Insight
##概要
AI Document Insightは、PDFファイルやWebサイトのコンテンツを解析し、重要な情報を抽出・要約するデスクトップアプリケーションです。

単にAI（LLM）に全てを任せるのではなく、グラフ理論に基づくTextRankアルゴリズムによる数学的な情報圧縮と、Large Language Model (LLM) による自然な文章整形を組み合わせた、効率的で堅牢なハイブリッド解析パイプラインを採用しています。

##主な機能
PDF解析: PyMuPDFを使用した高速なテキスト抽出と構造分析。

Webスクレイピング: BeautifulSoup4によるWebサイト本文の自動取得。

ハイブリッド要約: TextRankでトークン消費を抑えつつ、Gemini APIで高品質な文章を生成。

キーワード抽出: 日本語形態素解析（spaCy）を用いた重要語句の特定。

モダンUI: CustomTkinterによる、直感的で応答性の高いダークモード対応UI。

##インストール
依存ライブラリのインストール

Bash
pip install customtkinter requests beautifulsoup4 pymupdf spacy numpy google-genai python-dotenv
自然言語処理モデルのダウンロード

Bash
python -m spacy download ja_core_news_sm
使い方
#APIキーの設定
ルートディレクトリに .env ファイルを作成し、Gemini APIキーを記述します。

コード スニペット
GEMINI_API_KEY=your_api_key_here
プロジェクトの実行

Bash
python modern_gui.py
解析の実行

URL解析: 入力欄にURLを貼り付け、「URL解析」ボタンを押下。

PDF解析: 「PDFを選択」ボタンからローカルのファイルを選択。

解析が完了すると、重要キーワードと要約文が自動的に表示されます。

##運用
このプロジェクトのフォークを作成します。

新しい機能の追加やバグ修正など、変更を加えます。

変更内容を記述し、プルリクエストを送信してください。

ライセンス
このプロジェクトは、MITライセンスの下でライセンスされています。