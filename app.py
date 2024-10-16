from flask import Flask, request, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('ABHIRANG.db')
    conn.row_factory = sqlite3.Row
    return conn

# 1. User Management
@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    username = data['username']
    password_hash = generate_password_hash(data['password_hash'])
    email = data['email']
    phone_number = data['phone_number']
    user_type = data['user_type']
    
    conn = get_db_connection()
    conn.execute('INSERT INTO "user" (username, password_hash, email, phone_number, user_type, is_verified) VALUES (?, ?, ?, ?, ?, 0)',
                 (username, password_hash, email, phone_number, user_type))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "User registered successfully."}), 201

@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    username = data['username']
    password_hash = data['password_hash']

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM "user" WHERE username = ?', (username,)).fetchone()
    conn.close()
    
    if user and check_password_hash(user['password_hash'], password_hash):
        return jsonify({"username": user['username'], "user_type": user['user_type'], "is_verified": user['is_verified']}), 200
    else:
        return jsonify({"message": "Invalid credentials."}), 401

@app.route('/verify_user/<username>', methods=['PUT'])
def verify_user(username):
    conn = get_db_connection()
    conn.execute('UPDATE "user" SET is_verified = 1 WHERE username = ?', (username,))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "User verified successfully."}), 200

# 2. Category Management
@app.route('/categories', methods=['GET'])
def list_categories():
    conn = get_db_connection()
    categories = conn.execute('SELECT name, description FROM "category"').fetchall()
    conn.close()
    
    return jsonify([dict(category) for category in categories]), 200

@app.route('/categories', methods=['POST'])
def add_category():
    data = request.json
    name = data['name']
    description = data['description']

    conn = get_db_connection()
    conn.execute('INSERT INTO "category" (name, description) VALUES (?, ?)', (name, description))
    conn.commit()
    conn.close()

    return jsonify({"message": "Category added successfully."}), 201

# 3. Product Management
@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    name = data['name']
    description = data['description']
    price = data['price']
    stock_quantity = data['stock_quantity']
    category_id = data['category_id']
    artist_id = data['artist_id']
    dimensions = data.get('dimensions')
    medium = data.get('medium')
    image_url = data.get('image_url')

    conn = get_db_connection()
    conn.execute('INSERT INTO "product" (name, description, price, stock_quantity, category_id, artist_id, dimensions, medium, image_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                 (name, description, price, stock_quantity, category_id, artist_id, dimensions, medium, image_url))
    conn.commit()
    conn.close()

    return jsonify({"message": "Product added successfully."}), 201

@app.route('/products/<category_id>', methods=['GET'])
def list_products_by_category(category_id):
    conn = get_db_connection()
    products = conn.execute('SELECT name, description, price, stock_quantity FROM "product" WHERE category_id = ?', (category_id,)).fetchall()
    conn.close()
    
    return jsonify([dict(product) for product in products]), 200

@app.route('/products/<product_name>', methods=['GET'])
def product_details(product_name):
    conn = get_db_connection()
    product = conn.execute('SELECT p.name, p.description, p.price, p.stock_quantity, p.rating, c.name AS category_name, u.username AS artist_name FROM "product" p JOIN "category" c ON p.category_id = c.category_id JOIN "user" u ON p.artist_id = u.user_id WHERE p.name = ?', (product_name,)).fetchone()
    conn.close()
    
    return jsonify(dict(product)) if product else jsonify({"message": "Product not found."}), 404

# 4. Cart and Order Management
@app.route('/cart/<user_id>', methods=['GET'])
def view_cart(user_id):
    conn = get_db_connection()
    items = conn.execute('SELECT ci.cart_id, p.name, ci.quantity, ci.price_per_unit, (ci.quantity * ci.price_per_unit) AS total_price FROM "Cart_Item" ci JOIN "Cart" c ON ci.cart_id = c.cart_id JOIN "product" p ON ci.product_id = p.product_id WHERE c.user_id = ?', (user_id,)).fetchall()
    conn.close()
    
    return jsonify([dict(item) for item in items]), 200

@app.route('/cart/<cart_id>', methods=['POST'])
def add_to_cart(cart_id):
    data = request.json
    product_id = data['product_id']
    quantity = data['quantity']
    price_per_unit = data['price_per_unit']

    conn = get_db_connection()
    conn.execute('INSERT INTO "Cart_Item" (cart_id, product_id, quantity, price_per_unit) VALUES (?, ?, ?, ?)', (cart_id, product_id, quantity, price_per_unit))
    conn.commit()
    conn.close()

    return jsonify({"message": "Item added to cart successfully."}), 201

@app.route('/order', methods=['POST'])
def place_order():
    data = request.json
    user_id = data['user_id']
    total_amount = data['total_amount']

    conn = get_db_connection()
    conn.execute('INSERT INTO "Order" (user_id, order_date, total_amount, order_status) VALUES (?, CURRENT_TIMESTAMP, ?, "pending")', (user_id, total_amount))
    conn.commit()
    conn.close()

    return jsonify({"message": "Order placed successfully."}), 201

@app.route('/order_items/<order_id>', methods=['POST'])
def add_order_items(order_id):
    data = request.json
    product_id = data['product_id']
    quantity = data['quantity']
    price_per_unit = data['price_per_unit']

    conn = get_db_connection()
    conn.execute('INSERT INTO "Order_Item" (order_id, product_id, quantity, price_per_unit) VALUES (?, ?, ?, ?)', (order_id, product_id, quantity, price_per_unit))
    conn.commit()
    conn.close()

    return jsonify({"message": "Order items added successfully."}), 201

# 5. Commission Management
@app.route('/commissions', methods=['POST'])
def request_commission():
    data = request.json
    user_id = data['user_id']
    artist_id = data['artist_id']
    description = data['description']
    agreed_price = data['agreed_price']
    deadline = data['deadline']

    conn = get_db_connection()
    conn.execute('INSERT INTO "Commission" (user_id, artist_id, description, agreed_price, status, deadline, created_at) VALUES (?, ?, ?, ?, "pending", ?, CURRENT_TIMESTAMP)',
                 (user_id, artist_id, description, agreed_price, deadline))
    conn.commit()
    conn.close()

    return jsonify({"message": "Commission requested successfully."}), 201

@app.route('/commissions/<commission_id>', methods=['PUT'])
def update_commission_status(commission_id):
    data = request.json
    status = data['status']
    artist_id = data['artist_id']

    conn = get_db_connection()
    conn.execute('UPDATE "Commission" SET status = ? WHERE commission_id = ? AND artist_id = ?', (status, commission_id, artist_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Commission status updated successfully."}), 200

# 6. Insurance Management
@app.route('/insurance', methods=['POST'])
def add_insurance():
    data = request.json
    commission_id = data['commission_id']
    coverage_details = data['coverage_details']
    price = data['price']
    terms = data['terms']

    conn = get_db_connection()
    conn.execute('INSERT INTO "Insurance" (commission_id, is_insured, coverage_details, price, terms, created_at) VALUES (?, 1, ?, ?, ?, CURRENT_TIMESTAMP)',
                 (commission_id, coverage_details, price, terms))
    conn.commit()
    conn.close()

    return jsonify({"message": "Insurance added successfully."}), 201

# 7. Review Management
@app.route('/reviews', methods=['POST'])
def add_review():
    data = request.json
    product_id = data['product_id']
    user_id = data['user_id']
    rating = data['rating']
    comment = data['comment']

    conn = get_db_connection()
    conn.execute('INSERT INTO "Review" (product_id, user_id, rating, comment, created_at) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)',
                 (product_id, user_id, rating, comment))
    conn.commit()
    conn.close()

    return jsonify({"message": "Review added successfully."}), 201

@app.route('/reviews/<product_id>', methods=['GET'])
def view_reviews(product_id):
    conn = get_db_connection()
    reviews = conn.execute('SELECT r.rating, r.comment, r.created_at, u.username FROM "Review" r JOIN "user" u ON r.user_id = u.user_id WHERE r.product_id = ? ORDER BY r.created_at DESC', (product_id,)).fetchall()
    conn.close()
    
    return jsonify([dict(review) for review in reviews]), 200

# 8. Artist Portfolio Management
@app.route('/portfolio', methods=['POST'])
def add_artwork_to_portfolio():
    data = request.json
    artist_id = data['artist_id']
    artwork_name = data['artwork_name']
    description = data['description']
    medium = data['medium']
    image_url = data['image_url']

    conn = get_db_connection()
    conn.execute('INSERT INTO "Artist_Portfolio" (artist_id, artwork_name, description, medium, image_url, created_at) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)',
                 (artist_id, artwork_name, description, medium, image_url))
    conn.commit()
    conn.close()

    return jsonify({"message": "Artwork added to portfolio successfully."}), 201

@app.route('/portfolio/<artist_id>', methods=['GET'])
def view_artist_portfolio(artist_id):
    conn = get_db_connection()
    portfolio = conn.execute('SELECT artwork_name, description, medium, image_url FROM "Artist_Portfolio" WHERE artist_id = ?', (artist_id,)).fetchall()
    conn.close()
    
    return jsonify([dict(artwork) for artwork in portfolio]), 200

# 9. Admin Dashboard Queries
@app.route('/admin/dashboard', methods=['GET'])
def admin_dashboard():
    conn = get_db_connection()
    stats = conn.execute('SELECT COUNT(username) AS total_users, COUNT(CASE WHEN created_at >= DATE("now", "-1 month") THEN 1 END) AS new_users_last_month FROM "user"').fetchone()
    conn.close()
    
    return jsonify(dict(stats)), 200

@app.route('/admin/top_selling_products', methods=['GET'])
def top_selling_products():
    conn = get_db_connection()
    products = conn.execute('SELECT p.name, COUNT(oi.order_id) AS total_sold, SUM(oi.price_per_unit * oi.quantity) AS total_revenue FROM "product" p JOIN "Order_Item" oi ON p.product_id = oi.product_id GROUP BY p.name ORDER BY total_sold DESC LIMIT 10').fetchall()
    conn.close()
    
    return jsonify([dict(product) for product in products]), 200

# 10. Top-Selling Artist (Homepage)
@app.route('/top_selling_artist', methods=['GET'])
def top_selling_artist():
    conn = get_db_connection()
    artist = conn.execute('SELECT u.username AS artist_name, COUNT(o.order_id) AS total_orders FROM "user" u JOIN "product" p ON u.user_id = p.artist_id JOIN "Order_Item" oi ON p.product_id = oi.product_id JOIN "Order" o ON oi.order_id = o.order_id GROUP BY u.username ORDER BY total_orders DESC LIMIT 1').fetchone()
    conn.close()
    
    return jsonify(dict(artist)) if artist else jsonify({"message": "No orders found."}), 404

if __name__ == '__main__':
    app.run(debug=True)