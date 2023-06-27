import flet as ft

order_history = ft.DataTable(
                    heading_row_color = ft.colors.GREEN,
                    border=ft.border.all(10, ft.colors.GREEN),
                    columns=[
                        ft.DataColumn(ft.Text("ID")),
                        ft.DataColumn(ft.Text("DATE")),
                        ft.DataColumn(ft.Text("ITEM NO.")),
                        ft.DataColumn(ft.Text("PRODUCT")),
                        ft.DataColumn(ft.Text("TYPE")),
                        ft.DataColumn(ft.Text("PRICE")),
                        ft.DataColumn(ft.Text("QUANTITY")),
                        ft.DataColumn(ft.Text("TOTAL")),
                    ],
                    rows=[]
        )