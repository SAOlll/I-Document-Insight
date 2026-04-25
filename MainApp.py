import tkinter as tk
from tkinter import ttk, messagebox, filedialog
# 新しいモジュールをインポート
from pdf_handler import PDFHandler
from logic import TextAnalyzer
from utils import fetch_web_text
from thread_manager import AnalysisThread

class SummaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Text Summarizer (Multi-Source)")
        self.root.geometry("800x700")

        self.analyzer = TextAnalyzer()
        self._setup_ui()

    def _setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Web入力セクション ---
        ttk.Label(main_frame, text="WebサイトのURL:", font=("", 9, "bold")).pack(anchor=tk.W)
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=5)

        self.url_entry = ttk.Entry(url_frame)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # 修正：self.fetch_btn に代入する
        self.fetch_btn = ttk.Button(url_frame, text="URL解析", command=self._handle_url_analyze)
        self.fetch_btn.pack(side=tk.LEFT, padx=5)

        # --- PDF選択セクション ---
        ttk.Label(main_frame, text="またはローカルのPDFファイル:", font=("", 9, "bold")).pack(anchor=tk.W, pady=(10, 0))
        pdf_frame = ttk.Frame(main_frame)
        pdf_frame.pack(fill=tk.X, pady=5)

        # 修正：self.file_btn に代入する
        self.file_btn = ttk.Button(pdf_frame, text="PDFファイルを選択して解析", command=self._handle_pdf_analyze)
        self.file_btn.pack(side=tk.LEFT)

        # --- 共通の出力エリア ---
        ttk.Separator(main_frame, orient="horizontal").pack(fill=tk.X, pady=15)

        ttk.Label(main_frame, text="重要なキーワード:").pack(anchor=tk.W)
        self.keyword_label = ttk.Label(main_frame, text="-", font=("", 10, "bold"), foreground="blue")
        self.keyword_label.pack(anchor=tk.W, pady=5)

        ttk.Label(main_frame, text="要約結果:").pack(anchor=tk.W)
        self.result_text = tk.Text(main_frame, height=15)
        self.result_text.pack(fill=tk.BOTH, expand=True)

    def _handle_url_analyze(self):
        url = self.url_entry.get().strip()
        if not url: return
        text = fetch_web_text(url)
        self._execute_analysis(text)

    def _handle_pdf_analyze(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not file_path: return

        # 新モジュールを使用
        text = PDFHandler.extract_text(file_path)
        self._execute_analysis(text)

    def _execute_analysis(self, text):
        """解析処理をスレッドで実行する"""
        if text.startswith("Error"):
            messagebox.showerror("エラー", text)
            return

        # 1. 解析前にボタンを無効化し、ユーザーに待機を促す
        self.fetch_btn.config(state=tk.DISABLED)
        self.file_btn.config(state=tk.DISABLED)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, "現在解析中...しばらくお待ちください。")

        # 2. バックグラウンドで動かす処理を定義
        def task():
            # キーワード抽出と要約をまとめて行う
            keywords = self.analyzer.extract_keywords(text)
            summary = self.analyzer.summarize(text)
            return {"keywords": keywords, "summary": summary}

        # 3. 完了後の処理を定義
        def on_complete(result):
            # GUIの更新はメインスレッドで行う必要がある（tkinterの制約）
            self.root.after(0, lambda: self._update_ui_with_result(result))

        # 4. スレッド起動
        thread = AnalysisThread(task, on_complete)
        thread.start()

    def _update_ui_with_result(self, result):
        """スレッド終了後にGUIを更新する"""
        self.result_text.delete("1.0", tk.END)

        k_str = " / ".join([f"{w}({c})" for w, c in result["keywords"]])
        self.keyword_label.config(text=k_str)
        self.result_text.insert(tk.END, result["summary"])

        # ボタンを復帰させる
        self.fetch_btn.config(state=tk.NORMAL)
        self.file_btn.config(state=tk.NORMAL)
def main():
    """
    アプリケーションの起動エントリポイント
    """
    root = tk.Tk()
    # SummaryAppクラスをインスタンス化
    app = SummaryApp(root)
    # GUIのメインループを開始
    root.mainloop()

if __name__ == "__main__":
    # このファイルが直接実行されたときだけmain()を動かす
    # (他のファイルからimportされたときには動かないようにする)
    main()