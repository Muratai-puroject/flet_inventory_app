"""Flet 在庫管理アプリのクエリモジュール"""

import sqlite3
from typing import List, Tuple
from config import DB_NAME


def init_db() -> None:
    """
    SQLiteデータベースを初期化する関数。

    items テーブルが存在しない場合は作成する。
    テーブルには、商品ID、商品名、数量を含む。

    引数:
        None

    戻り値:
        None
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def get_items() -> List[Tuple[int, str, int]]:
    """
    データベースから論理削除されていない商品データを取得する

    引数:
        None

    戻り値:
        List[Tuple[int, str, int]]: 商品ID、商品名、数量からなるタプルのリスト。
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, name, quantity FROM items")
    rows = c.fetchall()
    conn.close()
    return rows


def add_item(name: str, quantity: int) -> None:
    """
    新しい商品をデータベースに登録する

    引数:
        name (str): 商品名。
        quantity (int): 商品の在庫数。

    戻り値:
        None
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO items (name, quantity) VALUES (?, ?)", (name, quantity))
    conn.commit()
    conn.close()


def update_item(item_id: int, name: str, quantity: int) -> None:
    """
    指定された商品IDに対応するレコードの名前と在庫数を更新する。

    引数:
        item_id (int): 更新対象の商品ID。
        name (str): 更新後の商品名。
        quantity (int): 更新後の在庫数。

    戻り値:
        None
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE items SET name = ?, quantity = ? WHERE id = ?", (name, quantity, item_id))
    conn.commit()
    conn.close()


def delete_item(item_id: int) -> None:
    """
    指定された商品IDのレコードを物理削除する。

    物理削除とは、データベースからレコード自体を完全に削除する方法。

    引数:
        item_id (int): 削除する対象の商品のID。

    戻り値:
        None
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

