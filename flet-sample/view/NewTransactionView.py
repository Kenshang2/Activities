import flet as ft
from functools import reduce
from controller.ProductController import get_products
from model.Product import Product
from view.components.ItemCard import ItemCard
from controller.OrderController import order_history
import datetime


cart_items: list[tuple[Product, int]] = []
total_list:list=[]
date = datetime.date.today()
customer_ids:list = []
customers = ft.Text(f'{0}', weight=ft.FontWeight.BOLD, size=20)
income_list: list = []
income_field = ft.Text(f'{0}', weight=ft.FontWeight.BOLD, size=20)
num_of_sales: list = []
total_sales = ft.Text(f'{0}', weight=ft.FontWeight.BOLD, size=20)

def new_transaction_page(page: ft.Page, view: ft.View):
    products: list[Product] = get_products()
    view.bgcolor = ft.colors.AMBER_100
    # selected_product: Product | None = None
    total: float = 0
    quantity: int = 1
    cash = ft.TextField(label="Input Cash", value=0)
    change: float = 0 
    change_field = ft.Text(f'Change: {0}')

    view.appbar = ft.AppBar(title=ft.Text('New Transaction'),
                            leading=ft.IconButton(icon=ft.icons.ARROW_BACK,
                                                  on_click=lambda _: page.go('/')),)

    vw_product_list = ft.GridView(
        expand=1,
        runs_count=5,
        max_extent=300,
        spacing=5,
        run_spacing=5,
    )
    vw_cartlist = ft.ListView(expand=1, spacing=10, padding=5, auto_scroll=True)

    vw_total = ft.Text(f'P {0}',
                       weight=ft.FontWeight.W_900,
                       size=30)
    num_of_items = ft.Text(f'{0}', color=ft.colors.WHITE, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, size=10)

    def on_item_click(product: Product):
        print('Hi')
        subtotal: float = product.price * quantity

        vw_quantity = ft.Text(f'x {quantity}', weight=ft.FontWeight.BOLD)
        vw_subtotal = ft.Text(f'P {subtotal}',
                              weight=ft.FontWeight.BOLD,
                              size=24)

        def on_plus(_):
            nonlocal quantity

            quantity = quantity if quantity >= product.stocks else quantity + 1
            subtotal = product.price * quantity
            print(quantity)
            vw_quantity.value = f'x {quantity}'
            vw_subtotal.value = f'P {subtotal}'
            page.update()

        def on_minus(_):
            nonlocal quantity
            quantity = quantity if quantity - 1 <= 0 else quantity - 1
            subtotal = product.price * quantity
            vw_quantity.value = f'x {quantity}'
            vw_subtotal.value = f'P {subtotal}'
            page.update()

        def on_confirm(_):
            nonlocal total
            nonlocal num_of_items
            cart_items.append((product, quantity))
            num_of_sales.append(quantity)

            # calculate total
            total = reduce(lambda acc, item:
                           acc + item[0].price * item[1],
                           cart_items,
                           0)
            set_cart_listview()
            vw_total.value = f'P {total}'
            num_of_items.value = f'{len(cart_items)}'
            dialog.open = False
            vw_total.update()
            dialog.update()
            page.update()


        def on_close(_):
            dialog.open = False
            dialog.update()

        dialog: ft.AlertDialog = ft.AlertDialog(
            title=ft.Text(
                f'{product.name}   -  P{product.price}   - x{product.stocks}'
            ),
            content=ft.Container(
                width=600,
                height=600,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Image(src=product.image, width=400, height=400),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.ElevatedButton('-', on_click=on_minus),
                                vw_quantity,
                                ft.ElevatedButton('+', on_click=on_plus),
                            ]
                        ),
                        vw_subtotal
                    ],
                )
            ),
            actions_alignment=ft.MainAxisAlignment.END,
            actions=[
                ft.TextButton('CANCEL', on_click=on_close),
                ft.TextButton('CONFIRM', on_click=on_confirm),
            ],
        )    
        page.dialog = dialog
        dialog.open = True
        page.update()

    def set_products_list() -> ft.GridView:
        cards = map(
            lambda x:
                ItemCard(product=x,
                         on_click=lambda: on_item_click(product=x),),
            products)

        vw_product_list.controls = list(cards)
        return vw_product_list

    def set_cart_listview():
        def remove_from_cart(_):
            nonlocal total
            i=vw_cartlist.controls.index(cards)
            del cart_items[i]
            vw_cartlist.controls.remove(cards)
            num_of_items.value = f'{len(cart_items)}'
            page.update()
            
            total = reduce(lambda acc, item:
                acc + item[0].price * item[1],
                cart_items,
                0)

            vw_total.value = f'P {total}'
            vw_total.update()
            page.update()
            vw_cartlist.update()
            
        def hover_delete(e):
            e.control.icon_color = "red" if e.data == "true" else ft.colors.YELLOW_ACCENT_400
            e.control.update()

        for x in cart_items:
            cards = ft.Container(
                            on_click=lambda: None,
                            bgcolor=ft.colors.GREEN,
                            border_radius=5,
                            padding=20,
                            margin=2,
                            content=ft.Row(
                                controls=[
                                    ft.Text(value=x[0].name,
                                            color=ft.colors.WHITE
                                            ),
                                    ft.Text(value=f'x {x[1]}',
                                            color=ft.colors.WHITE
                                            ),
                                    ft.Text(value=f'P {x[0].price}',
                                            color=ft.colors.WHITE
                                            ),
                                    ft.TextButton(icon=ft.icons.DELETE, icon_color=ft.colors.YELLOW_ACCENT_400, on_click=remove_from_cart, on_hover=hover_delete)
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                        )
        
        vw_cartlist.controls.append(cards)
        vw_cartlist.update()

    def cancel_payment(_):
        page.dialog = checkout_dlg
        checkout_dlg.open = False
        page.update()

    def error_msg_cash(_):
        page.snack_bar = ft.SnackBar(
            ft.Text('Input Proper Amount of Cash'),
            bgcolor=ft.colors.RED_ACCENT
        )
        page.snack_bar.open = True
        page.update()
    
    def confirm_payment(_):
        cash_amount = cash.value
        nonlocal total
        nonlocal change
        nonlocal quantity

        if cash_amount == '':
            error_msg_cash(_)
        else:
            cash_amount = float(cash.value)
            if cash_amount < total:
                error_msg_cash(_)
            else:
                if total == 0:
                    cart_empty_msg(_)
                else:
                    total_sales.value = f'{sum(num_of_sales)}'
                    change = cash_amount - total
                    change_field.value = f'Change: {change}'
                    cancel.text = 'Confirm'
                    cash.value = 0
                    total = 0
                    vw_total.value = f'P {0}'
                    customer_ids.append(1)
                    customers.value = f'{sum(customer_ids)}'

                    # adding to data table
                    order_history.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(f'[ {len(customer_ids)} ]')),
                                ft.DataCell(ft.Text(f'{date}')),
                                ft.DataCell(ft.Text('')),
                                ft.DataCell(ft.Text('')),
                                ft.DataCell(ft.Text('')),
                                ft.DataCell(ft.Text('')),
                                ft.DataCell(ft.Text('')),
                                ft.DataCell(ft.Text('')),
                            ],
                        )   
                    )
                    for i in cart_items:
                        x=ft.Text(f'{i[0].price * i[1]}')
                        total_list.append(float(x.value))
                        order_history.rows.append(
                            ft.DataRow(
                                        cells=[
                                            ft.DataCell(ft.Text("")),
                                            ft.DataCell(ft.Text('')),
                                            ft.DataCell(ft.Text(f'{i[0].id}')),
                                            ft.DataCell(ft.Text(f'{i[0].name}')),
                                            ft.DataCell(ft.Text(f'{i[0].product_type}')),
                                            ft.DataCell(ft.Text(f'{i[0].price}')),
                                            ft.DataCell(ft.Text(f'{i[1]}')),
                                            ft.DataCell(x),
                                        ],
                            )
                        )
                    total_sum = sum(total_list)
                    income_list.append(total_sum)
                    total_list.clear()
                    order_history.rows.append(
                            ft.DataRow(color=ft.colors.AMBER_100,
                                        cells=[
                                            ft.DataCell(ft.Text("")),
                                            ft.DataCell(ft.Text('')),
                                            ft.DataCell(ft.Text('')),
                                            ft.DataCell(ft.Text('')),
                                            ft.DataCell(ft.Text('')),
                                            ft.DataCell(ft.Text('')),
                                            ft.DataCell(ft.Text('TOTAL AMOUNT:', weight=ft.FontWeight.W_500)),
                                            ft.DataCell(ft.Text(f'P {total_sum}', weight=ft.FontWeight.BOLD, color=ft.colors.RED_ACCENT)),
                                        ],
                            )   
                    )
                    income_field.value = f'{sum(income_list)}'
                    cart_items.clear()
                    num_of_items.value = f'{len(cart_items)}'
                    vw_cartlist.controls.clear()
                    vw_cartlist.update()
                    vw_total.update()
                    checkout_dlg.update()
                    change_field.update()
                    page.update()
                

    cancel = ft.TextButton(text='Cancel', on_click=cancel_payment)
    checkout_dlg=ft.AlertDialog(
        modal=True,
        title=ft.Text("Input Cash:"),
        content=ft.Container(
            content=ft.Column(
                [
                    cash,
                    change_field
                ],
                height = 90,
            )
        ),
        actions_alignment=ft.MainAxisAlignment.END,
        actions=[
            cancel,
            ft.TextButton('Pay Now', on_click=confirm_payment),
        ],       
    )

    def cart_empty_msg(_):
        page.snack_bar = ft.SnackBar(ft.Text('Cart is Empty, Order First!'),bgcolor=ft.colors.RED_ACCENT)
        page.snack_bar.open = True
        page.update()

    def open_checkout(_):
        nonlocal total
        nonlocal change
        cancel.text = 'Cancel'
        cash.value = 0
        change = 0
        change_field.value = f'Change: {change}'
        if total == 0:
            cart_empty_msg(_)
        else:
            page.dialog = checkout_dlg
            checkout_dlg.open = True
            page.update()

    side_nav = ft.Container(
        bgcolor=ft.colors.AMBER_400,
        padding=20,
        content=ft.Column(
            controls=[
                ft.Column(controls=[
                    ft.Row(
                        [
                            ft.Text('TOTAL:'),
                            ft.Stack(
                                [   
                                    ft.Container(
                                        width=53,
                                        height=53,
                                        alignment=ft.alignment.Alignment(0, 0),
                                        content=ft.Icon(name=ft.icons.SHOPPING_CART, size=30),
                                    ),
                                    ft.Container(
                                        opacity=0.8,
                                        alignment=ft.alignment.Alignment(1, -1),
                                        width=53,
                                        content=ft.Container(
                                            shape=ft.BoxShape.CIRCLE,
                                            bgcolor=ft.colors.AMBER_400,
                                            padding=3,

                                            content=ft.Container(content=num_of_items,
                                                    bgcolor=ft.colors.RED_ACCENT,
                                                    shape=ft.BoxShape.CIRCLE,
                                                    width=20,
                                                    height=20,
                                                    alignment=ft.alignment.center
                                            )
                                        )
                                    )
                                ]
                            )  
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    vw_total,
                ]),
                ft.Container(
                    content=vw_cartlist,
                    height=400,
                    border=ft.border.all(2, ft.colors.BLACK),
                    border_radius=ft.border_radius.all(5)
                ),
                ft.Container(
                    content=ft.FilledButton('PAY NOW', width=1000, on_click=open_checkout),
                )
            ]
        )
    )
    side_nav.border_radius = ft.border_radius.BorderRadius(topLeft=30, topRight=0, bottomLeft=30, bottomRight=0)
    view.controls = [
        ft.ResponsiveRow(
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Column(col=9, controls=[set_products_list()]),

                ft.Column(col=3,
                          horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                          controls= [side_nav]
                )
            ]
        )

    ]
    

    return view