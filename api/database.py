import psycopg2
import os

class Connection:
    def __init__(self):
        try:
            postgres_bd = 'fastfoods'

            if os.getenv('SETTING') == 'testing':
                postgres_bd='postgres'

            self.connection = psycopg2.connect(dbname=postgres_bd,
                                            user='postgres',
                                            password='asiimwe',
                                            host='localhost',
                                            port='5432'
                                            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            print('Connected to database')

        except Exception as error:
            print(error)


    def create_tables(self):

        create_table = "CREATE TABLE IF NOT EXISTS users\
         ( user_id SERIAL PRIMARY KEY, username VARCHAR(10),\
          email VARCHAR(100), password VARCHAR(100), admin BOOLEAN NOT NULL);"
        self.cursor.execute(create_table)
        
        create_table = "CREATE TABLE IF NOT EXISTS menu \
			( item_id SERIAL PRIMARY KEY, foodname VARCHAR(15), price INTEGER);"
        self.cursor.execute(create_table)

        create_table = "CREATE TABLE IF NOT EXISTS orders \
			( order_id SERIAL PRIMARY KEY, \
			user_id INTEGER NOT NULL REFERENCES users(user_id), \
			item_id INTEGER NOT NULL REFERENCES menu(item_id), \
			quantity INTEGER, location VARCHAR(100), status VARCHAR(10));"
        self.cursor.execute(create_table)

    def add_user(self, username, email, password):
        query = "INSERT INTO users (username, email, password, admin) VALUES\
            ('{}', '{}', '{}', False);".format(username, email, password)
        self.cursor.execute(query)

   
    def put_food(self, foodname, price):
        query = "INSERT INTO menu (foodname, price) VALUES ('{}', '{}');"\
			.format(foodname, price)
        self.cursor.execute(query)

    def get_orders(self):
        query = "SELECT * FROM orders;"
        self.cursor.execute(query)
        orders = self.cursor.fetchall()
        return orders    

    def get_users(self):
        query = "SELECT * FROM users;"
        self.cursor.execute(query)
        users = self.cursor.fetchall()
        return users 

    def get_menu(self):
        query = "SELECT * FROM menu; "
        self.cursor.execute(query)
        menu = self.cursor.fetchall()
        return menu

    def get_specific_order(self, order_id):
        query = "SELECT * FROM orders WHERE {} = '{}';".format(order_id, order_id)
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        return user

    def get_user(self, column, value):
        query = "SELECT * FROM users WHERE {} = '{}';".format(column, value)
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        return user


    def place_order(self, user_id, item_id, quantity, location):
        query = "INSERT INTO orders (user_id, item_id, quantity, location, status) VALUES ('{}', '{}', '{}', '{}', 'pending');".format(user_id, item_id, quantity, location)
        self.cursor.execute(query)


    def update_order_status(self, order_id, status):
        query = "UPDATE orders SET status = '{}' WHERE order_id = '{}';\
		".format(status, order_id)
        self.cursor.execute(query)


    def get_order_history(self, user_id):
        query = "SELECT * FROM orders WHERE user_id = '{}';".format(user_id)
        self.cursor.execute(query)
        history = self.cursor.fetchall()
        return history

    def make_admin(self):
        query = "UPDATE users SET admin = {} WHERE user_id = '{}';\
		".format(True, 1)
        self.cursor.execute(query)

           

  
Connection() 


#Connection().create_tables()    
#Connection().put_food('beef', 1000)
#Connection().add_user('dorothy', 'dorotheeasiimwe@gmail.com', 'password')
#Connection().place_order(1, 1, 2, 'kampala')
#print(Connection().get_orders())
#print(Connection().get_users())
#print(Connection().get_menu())
#Connection().update_order_status(1, 'procesing')
#print(Connection().get_order_history(1))