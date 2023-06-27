jfrom getpass import getpass
from typing import List

class Product:
    name: str
    price: float
    brand: str
    stocks: int

    def __init__(self, name, price, brand, stocks):
        self.name = name
        self.price = price 
        self.brand = brand
        self.stocks = stocks

class CartItem:
    product: Product
    quantity: int

    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

products: List[Product] = [
    Product('Tanduay', 145, 'brand1', 125),
    Product('Water', 15, 'Brand2', 180),
    Product('Coke', 50, 'Brand3', 30),
    Product('Sisig', 65, 'Brand4', 60),
]

cart_items: List[CartItem] = []

def display_products():
    while True:
        for i, product in enumerate(products):
            print(f'{i + 1} {product.name, product.price}')

        i = input('Order: ')
        try:
            i = int(i)
            i -= 1
        except ValueError:
            print('Error: Invalid input. Please enter a number.')
            continue

        qty = input('Quantity: ')
        try:
            qty = int(qty)
        except ValueError:
            print('Error: Invalid input. Please enter a number.')
            continue

        item = products[i]
        cart_items.append(CartItem(item, qty))

        more_orders = input('Do you want to add more orders? (Y/N): ').lower()
        if more_orders == 'n':
            break

    print('Order Summary:')
    for item in cart_items:
        print(f'Product: {item.product.name} Quantity: {item.quantity}' )

    confirm_orders = input('Confirm orders? (Y/N): ').lower()
    if confirm_orders == 'y':
        display_main_menu()
    else:
        cart_items.clear()
        display_main_menu()

def display_cart():
    while True:
        for i, item in enumerate(cart_items):
            total_price = item.product.price * item.quantity
            print(f'{i + 1}. Product: {item.product.name} Quantity: {item.quantity} Sub Total:  {total_price}')

        i = input('Select item to edit (0 to cancel): ')
        try:
            i = int(i) - 1
            if i < 0 or i >= len(cart_items):
                break
        except ValueError:
            print('Error: Invalid input. Please enter a number.')
            continue

        item = cart_items[i]
        action = input('Edit quantity (A) or remove item (R)? ').lower()

        if action == 'a':
            qty = input('Enter new quantity: ')
            try:
                qty = int(qty)
                item.quantity = qty
            except ValueError:
                print('Error: Invalid input. Please enter a number.')
                continue
        elif action == 'r':
            cart_items.remove(item)

        more_edits = input('Do you want to edit more items? (Y/N): ').lower()
        if more_edits == 'n':
            break


def authentication():
    while True:
        print("Please Enter Your Username and Password")
        username = input('Username: ')
        password = getpass('Password: ')

        if username == 'roxas' and password == 'johnmichael':
            print('Authentication successful!')
            display_main_menu()
            break
        else:
            print('Incorrect username or password. Please try again.')

def user_input():
    while True:
        i = input('input: ')

        if i == '1':
            display_products()
            break
        elif i == '2':
            display_cart()
            break
        elif i == '3':
            pay_order()
            break
        else:
            print("Invalid input. Please choose an option from 1-3.")


def display_main_menu():
    while True:
        print("""
            Main Menu:
            -----------
            1. Show Available Products
            2. Show your Cart
            3. Pay 

        Please choose an option (1-3):
        """)
        user_input()
        break


def pay_order():
    total = 0
    total = float(total)

    for i in cart_items:
        total += i.product.price * i.quantity
    print(f'Total: {total}')
    while True:
        cash = input('Input Cash: ')
        cash = float(cash)
        if cash < total:
            print('Your money is not enough!')
        else:
            break
    change = cash - total
    print('Successfully Paid!', i.product.price * i.quantity)
    print(f'Your Change is: {change}')
    cart_items.clear()
    display_main_menu()

if __name__ == '__main__':
    print("""
 █████╗ ████████╗     ██████╗     ██████╗██████╗███╗   ████╗   ████████████╗   ██████████████╗   ██╗█████████████╗    ███████████████╗██████╗██████╗███████╗
██╔══████╔════██║    ██╔════╝    ██╔════██╔═══██████╗  ████║   ████╔════████╗  ██████╔════████╗  ████╔════██╔════╝    ██╔════╚══██╔══██╔═══████╔══████╔════╝
█████████║    ██║    ██║         ██║    ██║   ████╔██╗ ████║   ███████╗ ██╔██╗ █████████╗ ██╔██╗ ████║    █████╗      ███████╗  ██║  ██║   ████████╔█████╗  
██╔══████║    ██║    ██║         ██║    ██║   ████║╚██╗██╚██╗ ██╔██╔══╝ ██║╚██╗██████╔══╝ ██║╚██╗████║    ██╔══╝      ╚════██║  ██║  ██║   ████╔══████╔══╝  
██║  ██╚█████████████╚██████╗    ╚██████╚██████╔██║ ╚████║╚████╔╝█████████║ ╚███████████████║ ╚████╚█████████████╗    ███████║  ██║  ╚██████╔██║  █████████╗
╚═╝  ╚═╝╚═════╚══════╝╚═════╝     ╚═════╝╚═════╝╚═╝  ╚═══╝ ╚═══╝ ╚══════╚═╝  ╚═══╚═╚══════╚═╝  ╚═══╝╚═════╚══════╝    ╚══════╝  ╚═╝   ╚═════╝╚═╝  ╚═╚══════╝
                                                                                                                                                            
""")
    authentication()
  
    display_main_menu()
   


 

    

    
