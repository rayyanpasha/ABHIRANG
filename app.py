from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///abhirang.db'
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Change this in production
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Models based on the provided schema
class User(db.Model):
    username = db.Column(db.String(80), primary_key=True)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    user_type = db.Column(db.String(20), nullable=False)  # e.g., customer, artist, admin
    is_verified = db.Column(db.Boolean, default=False)  # Changed to Boolean

class Category(db.Model):
    name = db.Column(db.String(80), primary_key=True)
    description = db.Column(db.Text)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Added primary key
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Integer, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.String(80), db.ForeignKey('category.name'), nullable=False)
    artist_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, default=0)
    dimensions = db.Column(db.String(50))
    medium = db.Column(db.String(50))
    image_url = db.Column(db.String(255))

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Added primary key
    user_id = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Added primary key
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_per_unit = db.Column(db.Integer, nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Added primary key
    user_id = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_amount = db.Column(db.Integer, nullable=False)
    order_status = db.Column(db.String(50), nullable=False)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Added primary key
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_per_unit = db.Column(db.Integer, nullable=False)

class Commission(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Added primary key
    user_id = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)
    artist_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    agreed_price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default="Pending")
    deadline = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Insurance(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Added primary key
    commission_id = db.Column(db.Integer, db.ForeignKey('commission.id'), nullable=False)
    is_insured = db.Column(db.Boolean, nullable=False)  # Changed to Boolean
    coverage_details = db.Column(db.Text, nullable=True)
    price = db.Column(db.Integer, nullable=False)
    terms = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Added primary key
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ArtistPortfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Added primary key
    artist_id = db.Column(db.Integer, nullable=False)
    artwork_name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    medium = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# API Endpoints
# ... (rest of the API endpoints)

if __name__ == '__main__':
    with app.app_context():  # Ensure the application context is available
        db.create_all()  # Create database tables if they do not exist
    app.run(debug=True)