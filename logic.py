#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
文章解析エンジン：自然言語処理（NLP）を用いた重要文抽出およびキーワード抽出を行う。
TextRankアルゴリズムに基づき、文間の類似度をグラフ構造としてモデル化する。
"""

__author__ = 'KR'
__version__ = '1.2.0'
__date__ = '2026/1/24'


import spacy
import numpy as np
from collections import Counter

class TextAnalyzer:
    """
    文章の構造解析、要約、キーワード抽出を担うクラス。
    """
    def __init__(self):
        """
        spaCyの日本語モデルをロードする。未インストールの場合は自動ダウンロードを行う。
        """
        try:
            self.nlp = spacy.load("ja_core_news_sm")
        except OSError:
            import os
            os.system("python -m spacy download ja_core_news_sm")
            self.nlp = spacy.load("ja_core_news_sm")

    def _calculate_similarity(self, sent1, sent2):
        """"
        2つの文の間の類似度を計算する。
        ジャカード係数に文長の対数による重み付けを行い、単語の重複度を評価する。
        """
        words1 = set([t.text for t in sent1 if t.pos_ in ("NOUN", "VERB", "ADJ")])
        words2 = set([t.text for t in sent2 if t.pos_ in ("NOUN", "VERB", "ADJ")])

        if not words1 or not words2:
            return 0.0

        # ジャカード係数（共通単語数 / 全単語数）
        common = words1.intersection(words2)
        return len(common) / (np.log(len(words1)) + np.log(len(words2)) + 1)

    def summarize(self, text, ratio=0.3):
        """
        TextRankアルゴリズムを用いて、文章から重要な文を指定された割合で抽出する。
        """
        doc = self.nlp(text)
        sentences = [s for s in doc.sents if len(s.text.strip()) > 5]
        n = len(sentences)

        if n <= 3: return text

        # 1. 隣接行列（類似度行列）の作成
        # 全ての文の組み合わせに対して類似度を計算
        matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if i != j:
                    matrix[i][j] = self._calculate_similarity(sentences[i], sentences[j])

        # 2. TextRank（PageRank）の反復計算
        # 各文の「重要度スコア」を求める
        scores = np.ones(n)
        d = 0.85  # ダンピングファクター（PageRankの標準値）
        for _ in range(20):  # 20回反復して収束させる
            new_scores = np.ones(n) * (1 - d)
            for i in range(n):
                for j in range(n):
                    if matrix[j][i] > 0 and np.sum(matrix[j]) > 0:
                        new_scores[i] += d * matrix[j][i] / np.sum(matrix[j]) * scores[j]
            scores = new_scores

        # 3. スコアの高い文を抽出
        summary_count = max(1, int(n * ratio))
        top_indices = np.argsort(scores)[-summary_count:]

        # 元の文章の順序で並べ直して結合
        final_sentences = [sentences[i].text for i in sorted(top_indices)]
        return "".join(final_sentences)

    def extract_keywords(self, text, limit=5):
        """
        文章から頻出する名詞を抽出し、重要キーワードとしてリストアップする。
        """
        doc = self.nlp(text)
        nouns = [token.text for token in doc if token.pos_ == "NOUN" and not token.is_stop]
        return Counter(nouns).most_common(limit)