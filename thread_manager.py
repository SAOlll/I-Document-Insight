#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
スレッド管理モジュール：GUIメインスレッドをブロックせずに重い解析処理を実行するための
スレッドクラスを提供する。
"""

__author__ = 'KR'
__version__ = '1.2.0'
__date__ = '2026/1/24'



import threading

class AnalysisThread(threading.Thread):
    """
    解析タスクをバックグラウンドで実行し、完了後にコールバックを呼び出すスレッドクラス。
    """
    def __init__(self, task_func, on_complete_func):
        """
        スレッドを初期化する。

        引数:
            task_func: 実行したい解析処理の関数
            on_complete_func: 処理完了時に結果を受け取るコールバック関数
        """
        super().__init__()
        self.task_func = task_func
        self.on_complete_func = on_complete_func
        self.daemon = True  # アプリ終了時にスレッドも終了させる

    def run(self):
        """
        スレッドの実行メインループ。タスクを実行し、完了通知を行う。
        """
        # 重い処理を実行
        result = self.task_func()
        # 完了後のコールバックを実行（GUIスレッドに通知が必要な場合はここで調整）
        self.on_complete_func(result)