import datetime

from sqlalchemy.orm.exc import NoResultFound
from src.models import Product, Category, Cart, User, Bill, Order, session, engine


class UserActivity:
    """
    Complete user activity implementation for following actions

    - Users should be able to view the list of multiple categories.
    - Users should be able to view all the products under a particular category.
    - Users should be able to view product details.
    - Users should be able to add products to Cart.
    - Users should be able to buy multiple products from the Cart.
    - Users should be able to remove products from the Cart.
    - If the final billing amount is greater than Rs 10,000 then Rs 500 OFF should be given to the user.
    - If the final billing amount is less than Rs 10,000 then no discount should be given to the user.
    - Bill should be generated for multiple product purchases showing the actual amount, discounted
      amount, and the final amount.
    - Admin should be able to add categories and products.
    - Admin should be able to see details of the products added to the cart by the user.
    - Admin should be able to see all the bills generated by all the users.

    """

    def __init__(self):
        
        self.db = session
        self.cart_value = 0.0
        self.discount = 0.0
        self.sub_total = 0.0
        self.username = None
        self.user_id = None
        self.order_id = None

    def get_user_id(self):
        """
        get currently logged in user_id for global use.
        
        """
        if self.username:
            user = self.db.query(User).filter(User.username.ilike(self.username)).one()
            self.user_id = user.id

    def login(self, username, password):
        """
        Authenticating user with password
        
        """
        try:
            user = session.query(User).filter(User.username.ilike(username), User.password.ilike(password)).one()
            if user:
                return user
        except NoResultFound:
            return False

    def add_category(self, name:str):
        """
        Category Add function for Admin
        """
        try:
            category = Category(name=name)
            self.db.add(category)
            self.db.commit()
            print("Category '%s' added successfully\n" % name)
            return True
        except Exception:
            return False

    def add_product(self, name, description, price, category):
        """
       Product adding function for admin
        """
        try:
            category = self.db.query(Category).filter(Category.name.ilike(category)).one()
            new_product = Product(
                name=name,
                description=description,
                price=price,
                category_id=category.id
            )
            session.add(new_product)
            session.commit()
            print("\n'%s' added successfully\n" % name)
            return True
        except NoResultFound:
            return False

    def get_carts(self):
        """
        Admin only activity
        fetch all carts created by user
       
        """
        with engine.connect() as con:
            rs = con.execute('select user_id, group_concat(product_id) from cart group by user_id;')

            # check if cart exists
            if not rs.rowcount == -1:
                for row in rs:
                    # get username
                    user = self.db.query(User).filter(User.id.like(row[0])).one()
                    print("Cart created by '%s'" % user.username)
                    product_ids = row[1].split(',')

                    # get all products for user
                    for index, prod_id in enumerate(product_ids, start=1):
                        product = self.db.query(Product).filter(Product.id.like(int(prod_id))).one()
                        print(str(index) + "\t" + product.name)
                    print('-' * 50)
            else:
                print("No carts available yet")

    def get_bills(self):
        """
        admin only
        Fetch all bills generated for user
       
        """

        with engine.connect() as con:
            rs = con.execute(
                'select * from orders inner join bill on orders.id = bill.order_id where status = "Confirmed" order by user_id asc;'
            )
            bills = rs.fetchall()
            if bills:
                print("Ordered date \t\t\t Username \t\t\t Cart amount \t\t\t Discount \t\t\t Total \t\t\t Satus")
                print('-' * 110)
                for row in bills:
                    user = self.db.query(User).get(row[3])
                    order_date = str(row[1])
                    cart_amount = str(row[7])
                    discount = str(row[8])
                    total = str(row[9])
                    status = row[2]
                    details = "%s \t\t %s \t\t\t %s \t\t\t %s \t\t\t %s \t\t %s" % (
                        order_date[:-7], user.username, cart_amount, discount, total, status
                    )
                    print(details)
            else:
                print("\nNo bills available yet")

    def get_all_category(self):
        """
        Fetch all the category present in the db
     
        """
        cats = self.db.query(Category).all()
        for index, cat in enumerate(cats, start=1):
            print(str(index) + "\t" + cat.name)

    def get_products_by_category(self, category):
        """
        Filter product by provided category
       
        """
        try:
            category = self.db.query(Category).filter(Category.name.ilike(category)).one()
            for index, prod in enumerate(category.products, start=1):
                print(str(index) + '\t' + prod.name)
            return True
        except NoResultFound:
            print("Please select valid category name from list!!")
            return None

    def get_product(self, name):
        """
        Detail view for the product given by name
        
        """
        product = self.db.query(Product).filter(Product.name.ilike(name)).one()
        print("Name: " + product.name)
        print("Description: " + product.description)
        print("Price: " + str(product.price))

    def view_cart(self):
        """
        Let user to check the status of cart
     
        """
        carts = self.db.query(Cart).filter(Cart.user_id.like(self.user_id)).all()
        cart_total = 0
        if carts:
            header = "Sr \t Item \t\t\t\t Price"
            print(header)
            print('-' * 50)
            for index, item in enumerate(carts, start=1):
                prod_id = item.product_id
                product = self.db.query(Product).filter(Product.id.like(prod_id)).one()
                record = "{} \t {} \t\t\t {}".format(str(index), product.name, str(product.price))
                print(record)
                cart_total += product.price
            self.cart_value = cart_total
            print('-' * 50)
            print("Cart Total \t\t\t\t {}".format(str(self.cart_value)))
            return True
        print("Your cart is empty!!")
        return None

    def add_to_cart(self, product_name):
        """
        Add given product to the cart
       
        """
        product = self.db.query(Product).filter(Product.name.ilike(product_name)).one()
        item = self.db.query(Cart).filter(Cart.user_id.like(self.user_id)).filter(Cart.product_id.like(product.id)).all()

        # check whether item already exist in the cart
        if not item:
            cart = Cart(user_id=self.user_id, product_id=product.id)
            session.add(cart)
            session.commit()
            print("\n'%s' added to the cart" % product_name)
        else:
            print("\n'%s' is already present in the cart" % product_name)

    def remove_product(self, product_name):
        """
        Remove product from the cart
      
        """
        product = self.db.query(Product).filter(Product.name.ilike(product_name)).one()
        item = self.db.query(Cart).filter(Cart.product_id.like(product.id)).one()
        self.db.delete(item)
        self.db.commit()
        print("\n'%s' removed!" % product_name)
        return True

    def order_summary(self):
        """
        After placing order cart will be deleted
      
        """
        print("Here is your order summary\n")
        _ = self.view_cart()
        discount = 0
        self.sub_total = self.cart_value
        if self.cart_value >= 10000:
            self.cart_value -= 500
            self.discount = 500
            self.sub_total = self.cart_value - discount
            print('-' * 50)
            print("Coupon \t\t\t\t OFF500")
        print('-' * 50)
        print("Sub Total \t\t\t {}".format(str(self.sub_total)))

        # save the order
        order = Order(status='In Progress', user_id=self.user_id)
        self.db.add(order)
        self.db.commit()
        self.order_id = order.id

    def checkout(self):
        """
        Final buyout, generates bill
        and delete the user cart
  
        """
        try:

            print("Here is your final bill\n")
            _ = self.view_cart()
            print('-' * 27)
            print("Discount \t\t\t {}".format(str(self.discount)))
            print('-' * 27)
            print("Total \t\t\t {}".format(str(self.sub_total)))
            print("\nThanks for shopping!!")

            # delete the cart now
            carts = self.db.query(Cart).filter(Cart.user_id.like(self.user_id)).all()
            for item in carts:
                self.db.delete(item)
            self.db.commit()

            # change the order status and date
            order = self.db.query(Order).get(self.order_id)
            order.status = "Confirmed"
            order.order_date = datetime.datetime.now()
            self.db.commit()

            # save the bill to db
            bill = Bill(cart_value=self.cart_value, discount=self.discount, sub_total=self.sub_total, order_id=self.order_id)
            self.db.add(bill)
            self.db.commit()

        except Exception:
            pass
