import sqlite3
import re

def validate_name(name):
    try:
        # Only allow letters and spaces
        return re.match(r'^[A-Za-z ]+$', name) is not None
    except Exception as e:
        print(f"Error validating name: {e}")
        return False

def validate_phone(phone):
    try:
        # Allow only digits, and expect a specific length (adjust as needed)
        return re.match(r'^\d{10}$', str(phone)) is not None
    except Exception as e:
        print(f"Error validating phone: {e}")
        return False

def validate_email(email):
    try:
        # A basic pattern for email validation
        return re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email) is not None
    except Exception as e:
        print(f"Error validating email: {e}")
        return False

def validate_location(location):
    try:
        # Allow letters, spaces, and maybe other characters based on your needs
        return re.match(r'^[A-Za-z ]+$', location) is not None
    except Exception as e:
        print(f"Error validating location: {e}")
def validate_password(password):      
    try:
        return re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$',password)is not None

            # Check if the password matches the pattern
    except ValueError as ve:
            print(f'Error: {ve}')


class shopping_cart:
    list_of_products = {'shirts': [30, 599],
                        'shorts': [20, 800],
                        'bants': [20, 400],
                         'shoes': [0, 750],
                          'hat': [15, 200],
                        'gloves': [10, 150],
                        'scarf': [25, 300],
                        'socks': [30, 100],
                        
                        'jacket': [10, 1200],
                        'jeans': [15, 900],
                        'glasses': [8, 250],
                        'watch': [12, 500],
                       
                        'guitar': [3, 1000],
                        'camera': [5, 1500]}
 

    def __init__(self, name, phone_no, email, address,password):
        self.name = name
        self.phone_no = phone_no
        self.email = email
        self.address = address
        self.password= password
        
        
        # Create and initialize the database
        self.conn = sqlite3.connect('databasenew.db')
        self.cursor = self.conn.cursor()
        self.initialize_database()
       
        # Fetch cart data from the database
        self.cursor.execute('SELECT product, quantity FROM carts WHERE user=?;', (self.name,))
        cart_data = self.cursor.fetchall()
        #login
        self.cursor.execute('''SELECT name ,password FROM customers;''')



# Initialize an empty dictionary to store cart data
        self.cart = {}

# Convert the fetched data into a dictionary
        for item in cart_data:
            product, quantity = item
            self.cart[product] = quantity
                                    
    # @classmethod
    def initialize_database(self):
        conn = sqlite3.connect('databasenew.db')
        cursor = conn.cursor()

        # Create a table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                name TEXT,
                phone_no INTEGER,
                email TEXT,
                address TEXT,
                password varchar(255)
                            
                
            
                );''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS carts (
                product TEXT,
                quantity INTEGER,
                total INTEGER,
                user TEXT
            );
        ''')
         # Check if the customer name already exists
        cursor.execute('SELECT name FROM customers WHERE name = ?', (self.name,))
        existing_customer = cursor.fetchone()

        if existing_customer:
            print(f'Customer with name "{self.name}" already exists. Loading existing data.')
        else:
            # Insert customer details into the database
            cursor.execute('''
                INSERT INTO customers VALUES (?, ?, ?, ?,?)
            ''', (self.name, self.phone_no, self.email, self.address,self.password))

        # Commit changes
        conn.commit()

        # Close cursor and connection
        cursor.close()
        conn.close()
  
        # cursor.execute('''select name,password from customers where name=?;''',(user))
   

    @classmethod
    def display_products(cls):
        print('Products available in the shop are:')
        print()
        print('Items', 'Quantity', 'Price')
        print('--------------------------------')
        for product in cls.list_of_products:
            print(product, cls.list_of_products[product][0], cls.list_of_products[product][1], sep='\t')

    def display_details(self):
        print('Your details are:')
        print(f'Name: {self.name}')
        print(f'Phone_no: {self.phone_no}')
        print(f'Email: {self.email}')
        print(f'Address: {self.address}')
        
         # Check if the customer name already exists
        self.cursor.execute('SELECT * FROM customers WHERE name = ?', (self.name,))
        existing_customer = self.cursor.fetchone()
        

        if existing_customer:
          print(f'Customer with name "{self.name}" already exists. Loading existing data.')

            # Retrieve cart details for the existing user
          self.cursor.execute('SELECT * FROM carts WHERE user = ?', (self.name,))
          cart_details = self.cursor.fetchall()
           
          if cart_details:
            print('\nProducts in your cart are:')
            print('\nItems   ', 'Quantity  ', 'Price')
            print('**************************')
            total = 0
            for item in cart_details:
                print(item[0], '   ', item[1], '    ', item[2])
                total += item[2]
            print('Total:', total)
          else:
            print('Your cart is empty')
        else:
          print('This user does not exist in the database.')
  
    def add_product(self):
        self.display_products()
        product = input('Enter the product name:')
        if product in self.list_of_products:
            print('product is available')
            qty = int(input('Enter the Quantity:'))
            if self.list_of_products[product][0] >= qty:
                print('Quantity is available')
                if product in self.cart:
                    self.cart[product] += qty
                else:
                    self.cart[product] = qty
                self.list_of_products[product][0] -= qty
                print('product added successfully')
                

                 # Now, insert values into the "carts" table
                total = self.list_of_products[product][1] * qty
                self.cursor.execute('''
                  INSERT INTO carts VALUES (?, ?, ?,?)
            ''', (product, qty, total,self.name)) 
                
                self.conn.commit()
            

            else:
                print(f'Quantity is not available!, only {self.list_of_products[product][0]} {product} are left')
        else:
            print('Product is not available in the shop')
    

 
    def remove_product(self):
      
       # Fetch cart data from the database
      self.cursor.execute('SELECT product, quantity FROM carts WHERE user=?', (self.name,))
      cart_data = self.cursor.fetchall()

      if  not self.cart:
        print('Your cart is empty!, cannot remove any products!')
      else:
        product_name = input('Enter the product name: ')
        for product, quantity in self.cart.items():
            if product == product_name:
                print('Product is present in the cart')
                quantity_to_remove = int(input('Enter the quantity to remove: '))
                if quantity >= quantity_to_remove:
                    print('Quantity is available')
                    self.cart[product] -= quantity_to_remove
                    self.list_of_products[product_name][0] += quantity_to_remove

                    # Remove values from the "carts" table
                    self.cursor.execute('''
                        DELETE FROM carts
                        WHERE product=? AND user=? AND rowid IN (
                            SELECT rowid FROM carts WHERE product=? AND user=? LIMIT ?
                        )
                    ''', (product_name, self.name, product_name, self.name, quantity_to_remove))

                    self.conn.commit()

                    if self.cart[product] == 0:
                        del self.cart[product]

                    print('Product removed successfully!')
                else:
                    print(f'Cannot remove! Only {quantity} {product_name} is present in your cart')
                break
        else:
            print('This product is not present in your cart')
    # @classmethod
    # def sinup(self):
#         a=input("Enter your name:")
#         b=int(input('Enter your phone_no:'))
#         c=input('Enter a your email:')
#         d=input('Enter your location:')
#         e=input('Enter a password:')
# #        Validate inputs
#         if not validate_name(a):
#            print("Invalid name. Please enter only letters and spaces.")

#         elif not validate_phone(b):
#             print("Invalid phone number. Please enter a 10-digit number.")

#         elif not validate_email(c):
#              print("Invalid email address.")

#         elif not validate_location(d):
#              print("Invalid location. Please enter only letters and spaces.")
# # Create and initialize the database
#         elif not validate_password(e):
#             print("Password is not strong enough. It must have at least 8 characters, including a letter and a digit.")
# # Create and initialize the database
#         else:
#             conn = sqlite3.connect('databasenew.db')
#             cursor = conn.cursor()
#             c1=shopping_cart(a,b,c,d,e) 
#     # c1=shopping_cart('sandhiya',6385367557,'sandhiya15@gmail.com','chennai','sandhiya15@') 
#             c1.main()
#     # c1.main(self.conn.commit())

   
                 
   
   
    def main(self):
        print('---------------------------WELCOME----------------------------')

        print()

        while True:
            option = int(input('''Enter                       
        1. To display all the products available in the shop.
        2. To display your details.
        3. To add a product into the cart.
        4. To remove the product from the cart.
        5. To save customer data and exit.
        Enter your option:'''))
            print('____________________________________________________________')
            if option == 1:
                self.display_products()
            elif option == 2:
                self.display_details()
            elif option == 3:
                self.add_product()
            elif option == 4:
                self.remove_product()
            elif option == 5:
                
                print('Thank You for shopping!')
                break
            else:
                print('Invalid option! Please choose again')
  
    
#     def sinup( self):  # c1.main(self.conn.commit()) 
#         a=input("Enter your name:")
#         b=int(input('Enter your phone_no:'))
#         c=input('Enter a your email:')
#         d=input('Enter your location:')
#         e=input('Enter a password:')
# # Validate inputs
#         if not validate_name(a):
#               print("Invalid name. Please enter only letters and spaces.")

#         elif not validate_phone(b):
#              print("Invalid phone number. Please enter a 10-digit number.")

#         elif not validate_email(c):
#             print("Invalid email address.")

#         elif not validate_location(d):
#              print("Invalid location. Please enter only letters and spaces.")
# # Create and initialize the database
#         elif not validate_password(e):
#              print("Password is not strong enough. It must have at least 8 characters, including a letter and a digit.")
# # Create and initialize the database
#         else:
#           conn = sqlite3.connect('databasenew.db')
#           cursor = conn.cursor()
#           c1=shopping_cart(a,b,c,d,e) 
#     # c1=shopping_cart('sandhiya',6385367557,'sandhiya15@gmail.com','chennai','sandhiya15@') 
#           c1.main()
    # c1.main(self.conn.commit())
          
#     def user_data(self):
     
#         while True:
#             option=int(input('''enter 
#                      1.TO login
#                      2.TO sinup'''))  
#             if option==1:
#                 user_name=input("enter a username:")
#                 password_login=input("enter a password:")
#                 f= self.cursor.execute('''select name,password from customers where name=?;''',(user_name))

#                 for item in f:
#                     if user_name==item:
#                       c1=shopping_cart()
#                       print(c1.main())
#                     else:
#                        print("user name,password is not correct try again")
#             elif option==2:
#                 self.sinup()

#             else:
#                 print("choose 1 or 2")

# c2=shopping_cart()
# c2.user_data()



a=input("Enter your name:")
b=int(input('Enter your phone_no:'))
c=input('Enter a your email:')
d=input('Enter your location:')
e=input('Enter a password:')
# Validate inputs
if not validate_name(a):
        print("Invalid name. Please enter only letters and spaces.")

elif not validate_phone(b):
        print("Invalid phone number. Please enter a 10-digit number.")

elif not validate_email(c):
        print("Invalid email address.")

elif not validate_location(d):
        print("Invalid location. Please enter only letters and spaces.")
# Create and initialize the database
elif not validate_password(e):
       print("Password is not strong enough. It must have at least 8 characters, including a letter and a digit.")
# Create and initialize the database
else:
          conn = sqlite3.connect('databasenew.db')
          cursor = conn.cursor()
          c1=shopping_cart(a,b,c,d,e) 
    # c1=shopping_cart('sandhiya',6385367557,'sandhiya15@gmail.com','chennai','sandhiya15@') 
          c1.main()
    # c1.main(self.conn.commit())

            