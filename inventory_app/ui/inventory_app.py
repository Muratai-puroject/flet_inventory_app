"""Flet 在庫管理アプリのUI管理モジュール"""

import flet as ft
import db.db as db
from config import (COL_NO_WIDTH, COL_NAME_WIDTH, COL_QTY_WIDTH, COL_EDIT_WIDTH,
                    COL_DELETE_WIDTH, ROW_HEIGHT,APP_TITLE, COLUMN_NAME1, COLUMN_NAME2,
                    COLUMN_NAME3, COLUMN_NAME4, COLUMN_NAME5, LABEL_NAME1, LABEL_NAME2,
                    BUTTON_NAME1, WINDOW_WIDTH, WINDOW_HEIGHT, INPUT_WIDTH, INPUT_HEIGHT,
                    TOOL_TIP1, TOOL_TIP2, TOOL_TIP3)


def create_column(title: str, width_px: int, numeric: bool = False) -> ft.DataColumn:
    """
    DataTable のヘッダー列（DataColumn）を作成する関数。

    引数:
        title (str): 列ヘッダーに表示するタイトル文字列。
        width_px (int): 列の幅（ピクセル単位）。
        numeric (bool): 数値列かどうか。True にすると右寄せされる。

    戻り値:
        ft.DataColumn: 指定された設定に基づいた DataColumn オブジェクト。
    """
    return ft.DataColumn(
        label=ft.Container(
            ft.Text(title, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
            alignment=ft.alignment.center,
            width=width_px,
        ),
        numeric=numeric
    )


class InventoryApp:
    """
    在庫管理アプリのUIを構築するクラス。

    Fletを用いて商品名・在庫数の登録・編集・削除を行うUIを構成し、
    SQLiteデータベースと連携してデータの表示・更新を行う。
    """
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = APP_TITLE
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.bgcolor = ft.colors.GREY_50
        self.page.window_width = WINDOW_WIDTH
        self.page.window_height = WINDOW_HEIGHT
        self.page.window_resizable = False
        self.page.window_maximizable = False

        self.name_input = ft.TextField(label=LABEL_NAME1, width=INPUT_WIDTH)
        self.qty_input = ft.TextField(label=LABEL_NAME2, width=INPUT_HEIGHT,
                                      keyboard_type=ft.KeyboardType.NUMBER)

        # tableの設定
        self.data_table = ft.DataTable(
            bgcolor=ft.colors.BLUE_GREY_100,
            border=ft.border.all(1, ft.colors.BLUE_GREY_200),
            vertical_lines=ft.BorderSide(1, ft.colors.BLUE_GREY_200),
            heading_row_color=ft.colors.BLUE_GREY_700,
            heading_row_height=36,
            border_radius=6,
            columns=[
                create_column(COLUMN_NAME1, COL_NO_WIDTH),
                create_column(COLUMN_NAME2, COL_NAME_WIDTH),
                create_column(COLUMN_NAME3, COL_QTY_WIDTH, numeric=True),
                create_column(COLUMN_NAME4, COL_EDIT_WIDTH),
                create_column(COLUMN_NAME5, COL_DELETE_WIDTH),
            ],
            rows=[]
        )

        self.build_ui()
        db.init_db()
        self.load_data()

    def build_ui(self) -> None:
        """
        画面のUIコンポーネント（タイトル、入力欄、データテーブル）を構築し、ページに追加する。

        引数:
            なし（self.page を利用）

        戻り値:
            なし
        """
        title = ft.Text(APP_TITLE, size=24, weight=ft.FontWeight.BOLD)
        register_btn = ft.ElevatedButton(BUTTON_NAME1, on_click=self.on_register)

        # 入力エリアを作成
        input_row = ft.Row(
            controls=[self.name_input, self.qty_input, register_btn],
            spacing=10
        )

        # 入力エリア、登録ボタン、tableを縦方向に配置
        self.page.add(
            ft.Column(controls=[title, input_row, self.data_table], spacing=10)
        )

    def load_data(self) -> None:
        """
        データベースから商品データを取得し、テーブルに表示する。

        引数:
            なし（self 内のコンポーネントを使用）

        戻り値:
            なし
        """
        self.data_table.rows.clear()
        items = db.get_items()
        for index, (item_id, name, qty) in enumerate(items, start=1):
            self.render_row(index, item_id, name, qty)
        self.page.update()

    def render_row(self, display_no: int, item_id: int, name: str, qty: int) -> None:
        """
        DBから取得したデータを元にtable行を作成。

        引数:
            display_no (int): 表示上の通番（No列用）。
            item_id (int): データベース上のアイテムID。
            name (str): 商品名。
            qty (int): 個数。

        戻り値:
            None
        """
        name_txt = ft.Text(name, text_align=ft.TextAlign.LEFT)
        qty_txt = ft.Text(str(qty), text_align=ft.TextAlign.LEFT)
        name_field = ft.TextField(value=name, visible=False, width=200)
        qty_field = ft.TextField(value=str(qty), visible=False, width=100,
                                 keyboard_type=ft.KeyboardType.NUMBER)

        def edit_click(_e: ft.ControlEvent) -> None:
            """
            編集ボタンクリック時に、表示用テキストを非表示にし、
            編集用のテキストフィールドを表示する。

            引数:
                e (ft.ControlEvent): ボタンクリックイベントオブジェクト

            戻り値:
                None
            """
            # 商品名・個数の表示用テキストを非表示
            name_txt.visible = False
            qty_txt.visible = False

            # 商品名・個数の編集用テキストを表示
            name_field.visible = True
            qty_field.visible = True

            # 編集ボタンを非表示
            edit_btn.visible = False

            # 保存ボタンを表示
            save_btn.visible = True

            # 画面を再表示
            self.page.update()

        def save_click(_e: ft.ControlEvent) -> None:
            """
            保存ボタンのクリックイベントハンドラ。
            入力値を検証し、データベースを更新して画面を再表示する。

            引数:
                e (ft.ControlEvent): クリックイベントオブジェクト（未使用だが、Fletの仕様上必要）

            戻り値:
                None
            """

            # バリエーションチェック
            if not name_field.value.strip() or not qty_field.value.isdigit():
                return

            # 編集後の値をDBに保存
            db.update_item(item_id, name_field.value.strip(), int(qty_field.value))

            # DBからデータを再取得
            self.load_data()

        def delete_click(_e: ft.ControlEvent) -> None:
            """
            削除ボタンのクリックイベントハンドラ。
            対象のデータを物理削除する。

            引数:
                e (ft.ControlEvent): クリックイベントオブジェクト（未使用だが、Fletの仕様上必要）

            戻り値:
                None
            """

            # DBから対象のデータを論理削除
            db.delete_item(item_id)

            # DBからデータを再取得
            self.load_data()

        # 「編集」、「保存」、「削除」ボタンを用意
        edit_btn = ft.IconButton(icon=ft.icons.EDIT, tooltip=TOOL_TIP1, on_click=edit_click)
        save_btn = ft.IconButton(icon=ft.icons.SAVE, tooltip=TOOL_TIP2, on_click=save_click,
                                 visible=False)
        delete_btn = ft.IconButton(icon=ft.icons.DELETE, tooltip=TOOL_TIP3, icon_color=ft.colors.RED,
                                   on_click=delete_click)

        # tableの一行分の設定を行う
        row = ft.DataRow(
            cells=[
                # 項目：「No」の設定
                ft.DataCell(
                    ft.Container(
                        ft.Text(str(display_no), text_align=ft.TextAlign.LEFT),
                        alignment=ft.alignment.center_left,
                        height=ROW_HEIGHT,
                    )
                ),
                # 項目：「商品名」の設定
                ft.DataCell(
                    ft.Container(
                        ft.Row(
                            [name_txt, name_field],
                            alignment=ft.MainAxisAlignment.START,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        alignment=ft.alignment.center_left,
                        height=ROW_HEIGHT,
                    )
                ),
                # 項目：「個数」の設定
                ft.DataCell(
                    ft.Container(
                        ft.Row(
                            [qty_txt, qty_field],
                            alignment=ft.MainAxisAlignment.START,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        alignment=ft.alignment.center_left,
                        height=ROW_HEIGHT,
                    )
                ),
                # 項目：「編集」の設定
                ft.DataCell(
                    ft.Container(
                        ft.Row([edit_btn, save_btn]),
                        alignment=ft.alignment.center_left,
                        height=ROW_HEIGHT,
                    )
                ),
                # 項目：「削除」の設定
                ft.DataCell(
                    ft.Container(
                        delete_btn,
                        alignment=ft.alignment.center_left,
                        height=ROW_HEIGHT,
                    )
                ),
            ]
        )

        self.data_table.rows.append(row)

    def on_register(self, _e: ft.ControlEvent) -> None:
        """
        登録ボタン押下時の処理。

        商品名と個数を入力フィールドから取得し、バリデーションを行った上で
        データベースに登録する。その後、入力フィールドを初期化し、画面を更新する。

        引数:
            e (ft.ControlEvent): イベントオブジェクト（Fletイベントコールバック用）

        戻り値:
            None
        """

        # 商品名・個数の入力フィールドから「空白」を削除した状態で値を取得する
        name = self.name_input.value.strip()
        qty = self.qty_input.value.strip()

        # バリエーションチェック
        if not name or not qty.isdigit():
            return

        # DBに値を登録する
        db.add_item(name, int(qty))

        # 入力フィールドを初期化
        self.name_input.value = ""
        self.qty_input.value = ""
        self.load_data()
