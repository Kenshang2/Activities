import flet as ft
from controller.OrderController import order_history
from view.NewTransactionView import customer_ids
from view.NewTransactionView import income_field
from view.NewTransactionView import total_sales
from view.NewTransactionView import customers
from view.NewTransactionView import num_of_sales

def history_page(page: ft.Page, view: ft.View):
    view.appbar = ft.AppBar(title=ft.Text('Purchase History'),
                            leading=ft.IconButton(icon=ft.icons.ARROW_BACK,
                                                  on_click=lambda _: page.go('/')),)
    
    view.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    view.scroll=ft.ScrollMode.ALWAYS

    def clear_history(_):
        income_field.value = f'{0}'
        customers.value = f'{0}'
        total_sales.value = f'{0}'
        order_history.rows.clear()
        num_of_sales.clear()
        customer_ids.clear()
        page.update()

    view.controls = [
        ft.TextButton('CLEAR HISTORY', on_click=clear_history, icon=ft.icons.DELETE_SWEEP_ROUNDED),
        ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        height=100,
                        width=200,
                        bgcolor=ft.colors.WHITE70,
                        content=ft.Column(
                            [
                                ft.Container(
                                    width=190,
                                    content=ft.Text('NUMBER OF SALES', weight=ft.FontWeight.BOLD, size=18, color=ft.colors.GREEN),
                                    border=ft.border.only(bottom=ft.border.BorderSide(1, "green")),
                                    padding=5,
                                    alignment=ft.alignment.center
                                ),
                                ft.Row([
                                    ft.Icon(name=ft.icons.BAR_CHART_ROUNDED, color=ft.colors.YELLOW_400),
                                    total_sales
                                ])
                            ]
                        ),
                        alignment=ft.alignment.center,
                        padding=10,
                        border=ft.border.all(2, ft.colors.BLACK),
                        border_radius=ft.border_radius.all(10)
                    ),

                    ft.Container(
                        height=100,
                        width=200,
                        bgcolor=ft.colors.WHITE70,
                        content=ft.Column(
                            [
                                ft.Container(
                                    width=190,
                                    content=ft.Text('CUSTOMERS', weight=ft.FontWeight.BOLD, size=20, color=ft.colors.GREEN),
                                    border=ft.border.only(bottom=ft.border.BorderSide(1, "green")),
                                    padding=5,
                                    alignment=ft.alignment.center
                                ),
                                ft.Row([
                                    ft.Icon(name=ft.icons.PERSON_ADD_ALT_1_ROUNDED, color=ft.colors.YELLOW_400),
                                    customers
                                ])
                                
                            ]
                        ),
                        alignment=ft.alignment.center,
                        padding=10,
                        border=ft.border.all(2, ft.colors.BLACK),
                        border_radius=ft.border_radius.all(10)
                    ),

                    ft.Container(
                        height=100,
                        width=200,
                        bgcolor=ft.colors.WHITE70,
                        content=ft.Column(
                            [
                                ft.Container(
                                    width=190,
                                    content=ft.Text('PROFIT', weight=ft.FontWeight.BOLD, size=20, color=ft.colors.GREEN),
                                    border=ft.border.only(bottom=ft.border.BorderSide(1, "green")),
                                    padding=5,
                                    alignment=ft.alignment.center
                                ),
                                ft.Row([
                                    ft.Icon(name=ft.icons.ATTACH_MONEY_ROUNDED, color=ft.colors.YELLOW_400),
                                    income_field
                                ])
                            ]
                        ),
                        alignment=ft.alignment.center,
                        padding=10,
                        border=ft.border.all(2, ft.colors.BLACK),
                        border_radius=ft.border_radius.all(10)
                    )
                    
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY
            ),
            width=1000
        ),
        order_history
    ]
    return view