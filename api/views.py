import datetime

import jwt
from flask import Flask, jsonify, make_response, request
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from .database import Connection
from .models import User

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
conn = Connection()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None

        if 'x-access-token' in request.headers:

            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401
            
        try:

            data = jwt.decode(token, app.config['SECRET_KEY'])

            db_user = conn.get_user('email', data['email'])
 
            current_user = User(db_user[0], db_user[1], db_user[2], 
                            db_user[3], db_user[4])
            current_user.admin = data['admin']
        except:
            return jsonify({'message':'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated



@app.route('/auth/signup', methods=['POST',])
def register_user():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = generate_password_hash(data['password'])


    if not type(username) == str:
        return 'Error: Username must be a string!!!'
    if not type(password) == str:
        return 'Error: Password must be a string!!!'
    if username.strip() == '':
        return 'Error: Username cannot be empty!!!'
    if password.strip() == '':
        return 'Error: Password cannot be empty!!!'

    conn.add_user(username, email, password)
    return jsonify({'message': 'New User has been created'}), 201


@app.route('/auth/login', methods=['POST'])
def login_user():
    new_username = request.json['username']
    new_password = request.json['password']
    new_user = conn.get_user('username', new_username)

    if not new_user:
        return (jsonify({'mesasge':'No such username in the database '}))

    user = User(new_user[0], new_user[1], new_user[2], new_user[3], new_user[4]) 

    if user.username == new_username and check_password_hash (user.password, new_password):

        token = jwt.encode({'email':user.email, 'admin':user.admin, 
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
        
        return jsonify({'token' : token.decode('UTF-8'), 'message':'User logged-in'}), 200
    
    return jsonify({'message':'Check your Credentials!!!'}) 
    

@app.route('/users/orders', methods=['POST'])
@token_required
def place_food_order(current_user):
    user_id = request.json['user_id']
    item_id = request.json['item_id']
    foodname = request.json['foodname']
    quantity = request.json['quantity']
    location = request.json['location']
    conn.place_order(user_id, item_id,foodname, quantity, location)
    return jsonify({'message': 'food order has been added'}), 201   

@app.route('/menu', methods=['POST'])
@token_required
def add_menu(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function'}), 403

    foodname = request.json['foodname']
    price = request.json['price']
    conn.put_food(foodname, price)
    return jsonify({'message': 'Food has been added'}), 201

@app.route('/menu', methods=['GET']) 
@token_required
def get_menu(current_user):
    foodlist = conn.get_menu()  
    return jsonify({'Available food': foodlist})

@app.route('/orders', methods=['GET'])
@token_required
def get_all_orders(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function'}), 403

    all_orders = conn.get_orders()  
    return jsonify({'all orders': all_orders})
    

@app.route('/orders/<int:orderId>', methods=['PUT'])
@token_required
def update_order_status(current_user,orderId):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function'}), 403

    status = request.json['status']
    conn.update_order_status(orderId, status)
    return jsonify({'status': 'your status has been updated'}), 200
    
@app.route('/users/orders/<int:userId>', methods=['GET'])
@token_required
def get_orders_history(current_user, userId):
    order_history = conn.get_order_history(userId)
    return jsonify({'orderId' : order_history})



