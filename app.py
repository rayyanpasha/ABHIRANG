from flask import Flask, jsonify, request
from helper import execute_query

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Define routes
@app.route("/")
def index():
    return 'Welcome to the Ikea!'

# 1. Get all users (GET /user)
@app.route("/users", methods = ["GET"])
def users():
    if request.method == "GET":
        user = execute_query("SELECT * FROM users")
        return user, 200

# 2. Get a user by ID (GET `/user/<int:user_id>`)   
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = execute_query(f'SELECT * FROM Users WHERE UserID = {user_id}')

    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user), 200

# 3. Get all products (GET `/products`)  
@app.route("/products", methods = ["GET"])
def users():
    if request.method == "GET":
        product = execute_query("SELECT * FROM products")
        return product, 200

#4. Get a product by ID (GET `/products/<int:product_id>`)
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = execute_query(f'SELECT * FROM Products WHERE ProductID = {product_id}')
    if not product:
        return jsonify({"message": "Product not found"}), 404
    return jsonify(product), 200

# 5. Get cart items by user ID (GET `/cart/<int:user_id>`)
@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart_by_user_id(user_id):
    cart_items = execute_query(f'SELECT * FROM CartItems WHERE UserID = {user_id}')
    if not cart_items:
        return jsonify({"message": "Cart is empty for this user"}), 404
    return jsonify([dict(item) for item in cart_items]), 200

# 6. Create a new user (POST /users)
@app.route('/users', methods=['POST'])
def create_user():
    # Check if request contains JSON data
    if not request.is_json:
        return jsonify({"message": "Request must be JSON"}), 400

    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    # Validate required fields
    if not username or not password or not email:
        return jsonify({"message": "Missing required fields"}), 400

    # Hash the password but I am not sure if it is working or not.
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    try:
        # Execute insert query
        execute_query("INSERT INTO Users (Username, PasswordHash, Email) VALUES (?, ?, ?)", 
                      (username, password_hash, email))
        
        # Get the last inserted user ID
        user_id = execute_query("SELECT last_insert_rowid() AS UserID")[0]['UserID']
        
        return jsonify({"message": "User created successfully", "user_id": user_id}), 201
    
    except sqlite3.IntegrityError:
        return jsonify({"message": "User already exists"}), 409
    except Exception as e:
        return jsonify({"message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug = False)

