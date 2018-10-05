# challenge_three

## Functionality
- Create user accounts that can signin/signout from the app.
- Place an order for food.
- Get list of orders.
- Get a specific order.
- Update the status of an order.
- Get the menu.
- Add food option to the menu.
- View the order history for a particular user.

## Endpoints

|Endpoint |Functionality |
|---------|:------------:|
|POST /auth/signup|Register a user| 
|POST /auth/login |Login a user |
|POST /users/orders |Place an order for foods |
|GET  /users/orders|Get the order history for a particular user|
| GET /orders/| Get all orders (Admin only) | 
|GET /orders/<orderId>|Fetch a specific order (Admin only)|
|PUT /orders/<orderId>|Update the status  of an order (Admin only)|
| GET /menu|Get available menu|
|POST /menu  | Add a meal option to the menu (Admin only) |
  
# Prerequisites
- Set up the postgresql database.
- Configure the database name, password and portnumber.

# installed packages
- python 3.7
``` 
$ pip install -r requirements.txt
```
# run server
``` 
$ python run.py
```
This site should now be running at (http://localhost:5000)

# Testing

