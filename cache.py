import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime, timedelta
import random

# Database name
db_name = 'ABHIRANG.db'

# Number of records to generate for each table
num_users = 50
num_products = 100
num_orders = 50
num_commissions = 25
num_reviews = 75
num_categories = 5

# Generating users
usernames = [f'user_{i}' for i in range(1, num_users + 1)]
password_hashes = ['hashed_password'] * num_users  # Placeholder for hashed passwords
emails = [f'user_{i}@example.com' for i in range(1, num_users + 1)]  # Ensure uniqueness
phone_numbers = [f'555-010{i % 100}' for i in range(1, num_users + 1)]  # Modulo for unique phone numbers
user_types = ['artist' if i % 2 == 0 else 'buyer' for i in range(num_users)]  # Alternate artist and buyer

users_df = pd.DataFrame({
    'username': usernames,
    'password_hash': password_hashes,
    'email': emails,
    'phone_number': phone_numbers,
    'user_type': user_types,
    'is_verified': [random.choice([0, 1]) for _ in range(num_users)]
})

# Generating categories
category_names = [f'Category {i}' for i in range(1, num_categories + 1)]
category_descriptions = [f'Description for Category {i}' for i in range(1, num_categories + 1)]

categories_df = pd.DataFrame({
    'name': category_names,
    'description': category_descriptions
})

# Generating products
product_names = [f'Art Piece {i}' for i in range(1, num_products + 1)]
product_descriptions = [f'Description of Art Piece {i}' for i in range(1, num_products + 1)]
prices = [random.randint(100, 10000) for _ in range(num_products)]
stock_quantities = [random.randint(1, 50) for _ in range(num_products)]
category_ids = [random.randint(1, num_categories) for _ in range(num_products)]
artist_ids = [random.choice(users_df[users_df['user_type'] == 'artist']['username'].index) + 1 for _ in range(num_products)]
ratings = [round(random.uniform(1, 5), 1) for _ in range(num_products)]
mediums = ['oil', 'watercolor', 'acrylic', 'digital', 'charcoal']
dimensions = ['24x36 in', '18x24 in', '30x40 in']

products_df = pd.DataFrame({
    'name': product_names,
    'description': product_descriptions,
    'price': prices,
    'stock_quantity': stock_quantities,
    'category_id': category_ids,
    'artist_id': artist_ids,
    'rating': ratings,
    'dimensions': [random.choice(dimensions) for _ in range(num_products)],
    'medium': [random.choice(mediums) for _ in range(num_products)],
    'image_url': [f'https://example.com/art_{i}.jpg' for i in range(1, num_products + 1)]
})

# Generating carts
carts_df = pd.DataFrame({
    'user_id': [random.randint(1, num_users) for _ in range(num_users)],
    'created_at': [datetime.now() - timedelta(days=random.randint(1, 30)) for _ in range(num_users)],
    'updated_at': [datetime.now() for _ in range(num_users)]
})

# Generating cart items
cart_items_df = pd.DataFrame({
    'cart_id': [random.randint(1, num_users) for _ in range(num_products)],
    'product_id': [random.randint(1, num_products) for _ in range(num_products)],
    'quantity': [random.randint(1, 5) for _ in range(num_products)],
    'price_per_unit': [random.randint(100, 10000) for _ in range(num_products)]
})

# Generating orders
order_dates = [datetime.now() - timedelta(days=random.randint(1, 60)) for _ in range(num_orders)]
total_amounts = [random.randint(100, 5000) for _ in range(num_orders)]
order_statuses = ['completed', 'pending', 'shipped', 'canceled']

orders_df = pd.DataFrame({
    'user_id': [random.randint(1, num_users) for _ in range(num_orders)],
    'order_date': order_dates,
    'total_amount': total_amounts,
    'order_status': [random.choice(order_statuses) for _ in range(num_orders)]
})

# Generating order items
order_items_df = pd.DataFrame({
    'order_id': [random.randint(1, num_orders) for _ in range(num_products)],
    'product_id': [random.randint(1, num_products) for _ in range(num_products)],
    'quantity': [random.randint(1, 5) for _ in range(num_products)],
    'price_per_unit': [random.randint(100, 10000) for _ in range(num_products)]
})

# Generating commissions
commissions_df = pd.DataFrame({
    'user_id': [random.randint(1, num_users) for _ in range(num_commissions)],
    'artist_id': [random.choice(users_df[users_df['user_type'] == 'artist']['username'].index) + 1 for _ in range(num_commissions)],
    'description': [f'Commission description {i}' for i in range(1, num_commissions + 1)],
    'agreed_price': [random.randint(200, 5000) for _ in range(num_commissions)],
    'status': [random.choice(['pending', 'in progress', 'completed']) for _ in range(num_commissions)],
    'deadline': [datetime.now() + timedelta(days=random.randint(1, 60)) for _ in range(num_commissions)],
    'created_at': [datetime.now() for _ in range(num_commissions)]
})

# Generating insurances
insurances_df = pd.DataFrame({
    'commission_id': [i + 1 for i in range(num_commissions)],
    'is_insured': [random.choice([0, 1]) for _ in range(num_commissions)],
    'coverage_details': [f'Coverage details {i}' for i in range(1, num_commissions + 1)],
    'price': [random.randint(100, 1000) for _ in range(num_commissions)],
    'terms': [f'Terms for insurance {i}' for i in range(1, num_commissions + 1)],
    'created_at': [datetime.now() for _ in range(num_commissions)]
})

# Generating reviews
reviews_df = pd.DataFrame({
    'product_id': [random.randint(1, num_products) for _ in range(num_reviews)],
    'user_id': [random.randint(1, num_users) for _ in range(num_reviews)],
    'rating': [random.randint(1, 5) for _ in range(num_reviews)],
    'comment': [f'Review comment {i}' for i in range(1, num_reviews + 1)],
    'created_at': [datetime.now() - timedelta(days=random.randint(1, 60)) for _ in range(num_reviews)]
})

# Generating artist portfolios
portfolios_df = pd.DataFrame({
    'artist_id': [random.choice(users_df[users_df['user_type'] == 'artist']['username'].index) + 1 for _ in range(num_products)],
    'artwork_name': [f'Artwork {i}' for i in range(1, num_products + 1)],
    'description': [f'Description for artwork {i}' for i in range(1, num_products + 1)],
    'medium': [random.choice(mediums) for _ in range(num_products)],
    'image_url': [f'https://example.com/portfolio_{i}.jpg' for i in range(1, num_products + 1)],
    'created_at': [datetime.now() - timedelta(days=random.randint(1, 60)) for _ in range(num_products)]
})

# Connecting to SQLite database
conn = sqlite3.connect(db_name)

# Saving data to the database
users_df.to_sql('user', conn, if_exists='append', index=False)
categories_df.to_sql('category', conn, if_exists='append', index=False)
products_df.to_sql('product', conn, if_exists='append', index=False)
carts_df.to_sql('Cart', conn, if_exists='append', index=False)
cart_items_df.to_sql('Cart_Item', conn, if_exists='append', index=False)
orders_df.to_sql('Order', conn, if_exists='append', index=False)
order_items_df.to_sql('Order_Item', conn, if_exists='append', index=False)
commissions_df.to_sql('Commission', conn, if_exists='append', index=False)
insurances_df.to_sql('Insurance', conn, if_exists='append', index=False)
reviews_df.to_sql('Review', conn, if_exists='append', index=False)
portfolios_df.to_sql('Artist_Portfolio', conn, if_exists='append', index=False)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data generated and imported successfully into ABHIRANG.db!")
