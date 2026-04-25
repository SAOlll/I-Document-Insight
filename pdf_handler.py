#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PDFドキュメントハンドラ：PyMuPDFライブラリを用いて、PDFファイルからのテキスト抽出を行う。
"""

__author__ = 'KR'
__version__ = '1.0.1'
__date__ = '2026/1/22'



import fitz  # PyMuPDF
from utils import clean_text  # utilsからクリーニング関数をインポート

class PDFHandler:
    """
    PDFファイルの読み込みとテキスト抽出に特化したユーティリティクラス。
    """
    @staticmethod
    def extract_text(file_path):
        """
        指定されたパスのPDFからテキストを抽出・結合し、クリーニング処理を施して応答する。
        """
        try:
            doc = fitz.open(file_path)
            raw_text = ""
            for page in doc:
                # "blocks"形式で抽出：[x0, y0, x1, y1, "text", block_no, block_type]
                blocks = page.get_text("blocks")
                for block in blocks:
                    # block[4] がテキスト内容
                    raw_text += block[4] + "\n"
            doc.close()

            # ここで一括クリーニング（無駄な空白・重複改行の削除）
            cleaned_result = clean_text(raw_text)

            if not cleaned_result.strip():
                return "Error: PDFから有効なテキストを抽出できませんでした。"

            return cleaned_result

        except Exception as e:
            return f"Error: PDF読み込み中に問題が発生しました ({str(e)})"