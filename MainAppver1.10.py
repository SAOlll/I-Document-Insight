#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AI Document Insight: PDFおよびWebサイトの要約解析を行うメインGUIプログラム。
CustomTkinterを用いたモダンなユーザーインターフェースを提供し、
バックグラウンドでの非同期解析処理を制御する。
"""

__author__ = 'KR'
__version__ = '1.1.2'
__date__ = '2026/1/24'


import customtkinter as ctk
from tkinter import filedialog, messagebox
from thread_manager import AnalysisThread
from pdf_handler import PDFHandler
from logic import TextAnalyzer
from utils import fetch_web_text
from llm_summarizer import LLMSummarizer
import customtkinter as ctk

# 外観モードとテーマの設定
ctk.set_appearance_mode("dark")  # "dark" or "light"
ctk.set_default_color_theme("blue")

class ModernSummaryApp(ctk.CTk):
    """
    アプリケーションのメインウィンドウクラス。
    UIの構築、イベントハンドリング、および解析スレッドの管理を行う。
    """
    def __init__(self):
        """
        アプリケーションの初期化を行う。
        親クラスの初期化、解析ロジックのインスタンス化、UI構築を順に行う。
        """
        # 1. 必ず最初に親クラスを初期化する
        super().__init__()

        self.title("AI Document Insight")
        self.geometry("900x750")

        # 2. ロジックの初期化はUIを作る前に行う
        try:
            self.analyzer = TextAnalyzer()
            self.llm = LLMSummarizer()
        except Exception as e:
            messagebox.showerror("初期化エラー", str(e))

        # 3. その後にUIを構築するメソッドを呼ぶ
        self._setup_ui()

    def _setup_ui(self):
        """
        ウィジェットの配置とレイアウト設定を行う内部メソッド。
        """
        # グリッドレイアウトの設定
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1) # テキストエリアを広げる

        # --- タイトル ---
        self.title_label = ctk.CTkLabel(self, text="AI要約・解析ツール", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=20)

        # --- 入力セクション（URL） ---
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.url_entry = ctk.CTkEntry(self.input_frame, placeholder_text="解析したいWebサイトのURLを入力...")
        self.url_entry.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="ew")

        self.url_btn = ctk.CTkButton(self.input_frame, text="URL解析", command=self._handle_url_analyze)
        self.url_btn.grid(row=0, column=1, padx=(5, 10), pady=10)

        # --- 入力セクション（ファイル） ---
        self.file_frame = ctk.CTkFrame(self)
        self.file_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.file_label = ctk.CTkLabel(self.file_frame, text="ローカルファイルから解析:")
        self.file_label.pack(side="left", padx=10)

        self.pdf_btn = ctk.CTkButton(self.file_frame, text="PDFを選択", fg_color="transparent", border_width=2, command=self._handle_pdf_analyze)
        self.pdf_btn.pack(side="left", padx=10, pady=10)

        # --- プログレスバー（UX改善） ---
        self.progressbar = ctk.CTkProgressBar(self)
        self.progressbar.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        self.progressbar.set(0) # 初期値は0

        # --- 出力セクション ---
        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.grid(row=4, column=0, padx=20, pady=20, sticky="nsew")
        self.output_frame.grid_columnconfigure(0, weight=1)
        self.output_frame.grid_rowconfigure(1, weight=1)

        self.kw_title = ctk.CTkLabel(self.output_frame, text="重要キーワード:", font=ctk.CTkFont(weight="bold"))
        self.kw_title.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

        self.kw_display = ctk.CTkLabel(self.output_frame, text="-", text_color="#3B8ED0")
        self.kw_display.grid(row=0, column=0, padx=(120, 10), pady=(10, 0), sticky="w")

        self.result_text = ctk.CTkTextbox(self.output_frame, font=ctk.CTkFont(family="Hiragino Sans", size=13))
        self.result_text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    def _handle_url_analyze(self):
        """
        URL入力フィールドからテキストを取得し、解析プロセスを開始する。
        """
        url = self.url_entry.get().strip()
        if not url: return
        text = fetch_web_text(url)
        self._execute_analysis(text)

    def _handle_pdf_analyze(self):
        """
        ファイルダイアログからPDFを選択し、テキストを抽出して解析を開始する。
        """
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not file_path: return
        text = PDFHandler.extract_text(file_path)
        self._execute_analysis(text)


    def _execute_analysis(self, text):
        """
        解析プロセスを制御するメインロジック。

        1. GUIのステータスを「解析中」に更新する。
        2. TextRankによる重要文抽出とLLMによる文章整形を組み合わせた
           ハイブリッド解析タスクを、別スレッドで安全に実行する。
        3. API制限（429 Error等）発生時には、抽出結果を直接表示する
           フォールバック処理を行う。
        """
        # ... GUIの更新処理 ...

        def task():
            """
            バックグラウンドスレッドで実行される解析タスク本体。
            呼び出し元：AnalysisThread
            """
        # 1. TextRankで抽出（これはローカル実行なので制限なし）
            important_text = self.analyzer.summarize(text, ratio=0.4)

            # 2. LLMで整形を試みる
            final_summary = self.llm.refine_summary(important_text)

            # 3. もしLLMがエラーを返したら、TextRankの結果をフォールバックとして採用
            if "Error" in final_summary:
                final_summary = f"【お知らせ】API制限により、抽出文をそのまま表示します。\n\n{important_text}"

            keywords = self.analyzer.extract_keywords(text)
            return {"keywords": keywords, "summary": final_summary}

        # UI状態の更新
        self.url_btn.configure(state="disabled")
        self.pdf_btn.configure(state="disabled")
        self.progressbar.configure(mode="indefinite")
        self.progressbar.start()
        self.result_text.delete("1.0", "end")
        self.result_text.insert("end", "解析中...")

        def on_complete(result):
            """
            スレッド完了時にメインスレッドへ通知を行うコールバック関数。
            """
            self.after(0, lambda: self._update_ui(result))

        thread = AnalysisThread(task, on_complete)
        thread.start()

    def _update_ui(self, result):
        """
        解析結果をGUIに反映し、ウィジェットの状態を復元する。

        引数:
            result (dict): {"keywords": list, "summary": str} の形式の解析結果
        """
        self.progressbar.stop()
        self.progressbar.configure(mode="determinate")
        self.progressbar.set(1) # 完了

        self.url_btn.configure(state="normal")
        self.pdf_btn.configure(state="normal")

        self.result_text.delete("1.0", "end")
        self.result_text.insert("end", result["summary"])

        k_str = " / ".join([f"{w}({c})" for w, c in result["keywords"]])
        self.kw_display.configure(text=k_str)

if __name__ == "__main__":
    """
    プログラムのエントリポイント。
    アプリケーションのインスタンスを生成し、メインループを開始する。
    """
    app = ModernSummaryApp()
    app.mainloop()