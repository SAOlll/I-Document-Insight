#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Webからのデータ取得や、テキストのクリーニングなどの汎用的な機能を実行する。
"""

__author__ = 'KR'
__version__ = '1.3.1'
__date__ = '2026/1/23'



import requests
from bs4 import BeautifulSoup
import re

def fetch_web_text(url):
    """
    指定されたURLのWebサイトにアクセスし、本文（<p>タグ）と思われる箇所のテキストを抜き出して取得する。
    """
    try:
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        soup = BeautifulSoup(response.text, 'html.parser')

        # 本文と思われるタグ（pタグなど）からテキストを抽出
        paragraphs = soup.find_all('p')
        text = " ".join([p.get_text() for p in paragraphs])
        return text
    except Exception as e:
        return f"エラーが発生しました: {e}"
def clean_text(text):
    """
    テキストから無駄な空白や重複した改行を削除する
    """
    if not text:
        return ""

    # 1. 行末・行頭の空白を削除
    text = "\n".join([line.strip() for line in text.splitlines()])

    # 2. 3連続以上の改行を2連続（1行あき）にまとめる
    text = re.sub(r'\n{3,}', '\n\n', text)

    # 3. 文中の連続する半角・全角スペースを1つにまとめる
    text = re.sub(r'[ 　]+', ' ', text)

    return text.strip()