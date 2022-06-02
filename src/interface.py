
"""
Terminal UI wrapper for my cart
"""

from src.activity import UserActivity
from utils import convert_float


class UserInterface:

    def __init__(self):
        self.user_act = UserActivity()

    @staticmethod
    def title(name):
        print('-' * 110)
        print(name.center(110))
        print('-' * 110)

    @staticmethod
    def user_menu():
        print('-' * 110)
        print("1. View Categories 2. View cart 3. Logout")

    @staticmethod
    def admin_menu():
        print('-' * 110)
        print("1. Add category 2. Add product  3. Check user carts  4. Check bills  5. Logout")

    @staticmethod
    def cart_menu():
        print('-' * 110)
        print("1. Remove product 2. Checkout 3. Cancel")

    @staticmethod
    def product_menu():
        print('-' * 110)
        print("1. Add to cart 2. Cancel ")

    def admin_ui(self):
        """
         Admin Screen
        """

        flag = True
        while flag:
            self.admin_menu()
            choice = input("Enter your choice: ")

            if choice == '1':
                self.title('ADD CATEGORY')
                new_category = input("Enter category name: ")
                self.user_act.add_category(name=new_category)
                self.user_act.get_all_category()

            elif choice == '2':
                self.title('ADD PRODUCT')
                name = input("Enter product name: ")
                description = input("Enter product description: ")
                price = input("Enter product price: ")
                float_price = convert_float(price)
                if isinstance(float_price, float):
                    print("\nPlease select category for this product: ")
                    self.user_act.get_all_category()
                    category = input("\nEnter category from above: (category name) ")
                    status = self.user_act.add_product(name=name, description=description, price=price, category=category)
                    if status is False:
                        print("\nSomething went wrong, please check your inputs")
                else:
                    print("\nPlease provide valid number!!")

            elif choice == '3':
                # show user carts
                self.title('User Carts')
                self.user_act.get_carts()

            elif choice == '4':
                self.title("USER BILLS")
                self.user_act.get_bills()

            elif choice == '5':
                flag = False

            else:
                print("\nPlease select valid option!!")

    def user_ui(self):

        flag = True
        while flag:

            self.user_menu()
            choice = input("Enter your choice (select number): ")

            if choice == '1':
                self.title('CATEGORIES')
                self.user_act.get_all_category()
                cat_choice = input("Select category: (category name) ")
                self.title("PRODUCTS")
                status = self.user_act.get_products_by_category(category=cat_choice)
                if status:
                    prod_name = input("Select Product: (product name) ")
                    self.title(prod_name.upper())

                    # product detail page
                    self.user_act.get_product(name=prod_name)
                    self.product_menu()
                    prod_choice = input("Enter your choice (select number): ")
                    if prod_choice == '1':
                        self.user_act.add_to_cart(product_name=prod_name)
                    elif prod_choice == '2':
                        continue

            elif choice == '2':
                self.title('MY CART')
                status = self.user_act.view_cart()

                if status:
                    self.cart_menu()
                    sub_choice = input("Enter your choice: ")
                    if sub_choice == '1':
                        product_name = input("Enter product name to remove: ")
                        self.user_act.remove_product(product_name)

                    elif sub_choice == '2':
                        self.title("ORDER SUMMARY")
                        self.user_act.order_summary()
                        self.title("CHECKOUT")
                        pay = input("Please type 'Buy Now' for checkout: ")
                        if pay == 'Buy Now':
                            self.title("ORDER CONFIRMED")
                            self.user_act.checkout()
                        else:
                            continue

                    elif sub_choice == '3':
                        continue

            elif choice == '3':
                flag = False

            else:
                print("\nPlease select valid option!!")