import unittest

from src.models import User, session, Cart, Product
from src.interface import UserInterface
from src.activity import UserActivity


class TestAdminActivity(unittest.TestCase):

    ui = UserInterface()
    activity = UserActivity()

    def test_login(self):
        username = input("Username: ")
        password = input("Password: ")
        user = self.activity.login(username, password)
        return self.assertIsInstance(user, User)

    def test_add_category(self):
        category = input("Category: ")
        result = self.activity.add_category(category)
        return self.assertTrue(result, True)

    def test_add_product(self):
        price = float(input("Price: "))
        if isinstance(price, float):
            self.assertIsInstance(price, float)

        result = self.activity.add_product(
            name='test_product',
            description='this is test product',
            price=price,
            category='test_cat'
        )
        return self.assertTrue(result, True)


class TestUserActivity(unittest.TestCase):

    ui = UserInterface()
    activity = UserActivity()

    def test_checkout(self):
        order = "Confirmed"
        self.activity.checkout()
        if order == "Confirmed":
            return self.assertTrue(order, True)

    def test_remove_product(self):
        user_id = int(input('user id: '))
        carts = session.query(Cart).filter(Cart.user_id.like(user_id)).all()
        if carts:
            for item in carts:
                prod_id = item.product_id
                product = session.query(Product).filter(Product.id.like(prod_id)).one()
                print(product.name)
            product_name = input("Select product from above")
            status = self.activity.remove_product(product_name=product_name)
            self.assertTrue(status, True)
        else:
            print("Cart is empty")


if __name__ == "__main__":
    unittest.main()

