#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
文章解析エンジン：自然言語処理（NLP）を用いた重要文抽出およびキーワード抽出を行う。
TextRankアルゴリズムに基づき、文間の類似度をグラフ構造としてモデル化する。
"""

__author__ = 'KR'
__version__ = '1.1.2'
__date__ = '2026/1/24'

import os
from google import genai
from dotenv import load_dotenv
from utils import clean_text

class LLMSummarizer:
    """
    Gemini APIとの通信およびプロンプト制御を行うクラス。
    """
    def __init__(self):
        """
        環境変数の読み込みとクライアントの初期化。
        """
        # .envファイルから環境変数を読み込む
        load_dotenv()

        # 環境変数からAPIキーを取得
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            # キーがない場合はエラーを投げる
            raise ValueError("環境変数 'GEMINI_API_KEY' が設定されていません。")

        # クライアントの初期化
        self.client = genai.Client(api_key=api_key)
        # モデル名
        self.model_name = 'gemini-3-flash-preview'

    def refine_summary(self, extracted_text):
        """
        抽出された重要文を、自然な文章にまとめ直す
        """
        if not extracted_text:
            return "Error: 要約対象のテキストがありません。"

        prompt = f"""
        以下の文章は、ある文書から抽出された一節です。
        これらを元に、内容を保持したまま要約してください。

        ---
        {extracted_text}
        ---
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
                    )
        # 取得したテキストをクリーニングしてから返す
            return clean_text(response.text)
        except Exception as e:
                    return f"Error (LLM): {str(e)}"