from flask import Flask, jsonify, request 
app = Flask(__name__)
from database import Connection
from werkzeug.security import generate_password_hash

conn = Connection()

@app.route('/auth/signup', methods=['POST',])
def register_user():
    username = request.json['username']
    email = request.json['email']
    password = generate_password_hash(request.json['password'])
    conn.add_user(username, email, password)
    return jsonify({'message': 'User has been created'}), 201

@app.route('/auth/login', methods=['POST'])
def login_user():
    pass

@app.route('/users/orders', methods=['POST'])
def place_food_order():
    user_id = request.json['user_id']
    item_id = request.json['item_id']
    quantity = request.json['quantity']
    location = request.json['location']
    conn.place_order(user_id, item_id, quantity, location)
    return jsonify({'message': 'food order has been added'}), 201   

@app.route('/menu', methods=['POST'])
def add_menu():
    foodname = request.json['foodname']
    price = request.json['price']
    conn.put_food(foodname, price)
    return jsonify({'message': 'Food has been added'}), 201

@app.route('/menu', methods=['GET'])
def get_menu():
    foodlist = conn.get_menu()  
    return jsonify({'Available food': foodlist})

@app.route('/orders', methods=['GET'])
def get_all_orders():
    all_orders = conn.get_orders()  
    return jsonify({'all orders': all_orders})
    
# @app.route('/users/orders/orderId', methods=['GET'])
# def get_specific_order():
#     specific_order = conn.get_an_order(, value)  
#     return jsonify({'all orders': specific_order})


@app.route('/orders/<orderId>', methods=['PUT'])
def update_order_status():
    pass    
    
@app.route('/users/orders', methods=['GET'])
def get_orders_history():
    order_history = conn.get_order_history
    return jsonify({'my orders' : order_history})   



if __name__ == '__main__':
    app.run() 