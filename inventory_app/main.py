"""Flet 在庫管理アプリのメイン起動モジュール"""

import os
import sys
import signal
import flet as ft
from ui.inventory_app import InventoryApp


def main(page: ft.Page) -> None:
    """
    Fletアプリケーションのエントリーポイント関数。

    引数:
        page (ft.Page): Fletのページオブジェクト。アプリのUIコンテナ。

    戻り値:
        None
    """
    InventoryApp(page)

if __name__ == "__main__":
    try:
        ft.app(target=main)
    except RuntimeError as e:
        if "Event loop is closed" not in str(e):
            raise
    finally:
        # Windowsで"Event loop is closed"などが表示されるのを防止するためプロセスを終了
        if sys.platform.startswith("win"):
            os.kill(os.getpid(), signal.SIGTERM)
