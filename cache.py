import sqlite3
from datetime import datetime, timedelta
import random

# Function to generate random datetime
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('AbhiRang.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
cursor = conn.cursor()

# Register adapters and converters for datetime
def adapt_datetime(ts):
    return ts.strftime('%Y-%m-%d %H:%M:%S')

def convert_datetime(ts_bytes):
    return datetime.strptime(ts_bytes.decode('utf-8'), '%Y-%m-%d %H:%M:%S')

sqlite3.register_adapter(datetime, adapt_datetime)
sqlite3.register_converter('timestamp', convert_datetime)

# Create tables
cursor.executescript('''
CREATE TABLE IF NOT EXISTS "user" (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password_hash TEXT,
    email TEXT,
    phone_number TEXT,
    user_type TEXT,
    is_verified INTEGER
);

CREATE TABLE IF NOT EXISTS "category" (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS "product" (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    price INTEGER,
    stock_quantity INTEGER,
    category_id INTEGER,
    artist_id INTEGER,
    rating REAL,
    dimensions TEXT,
    medium TEXT,
    image_url TEXT,
    FOREIGN KEY (category_id) REFERENCES category(category_id)
);

CREATE TABLE IF NOT EXISTS "Cart" (
    cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE IF NOT EXISTS "Cart_Item" (
    cart_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cart_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    price_per_unit INTEGER,
    FOREIGN KEY (cart_id) REFERENCES Cart(cart_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);

CREATE TABLE IF NOT EXISTS "Order" (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    order_date TIMESTAMP,
    total_amount INTEGER,
    order_status TEXT,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE IF NOT EXISTS "Order_Item" (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    price_per_unit INTEGER,
    FOREIGN KEY (order_id) REFERENCES "Order"(order_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);

CREATE TABLE IF NOT EXISTS "Commission" (
    commission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    artist_id INTEGER,
    description TEXT,
    agreed_price INTEGER,
    status TEXT,
    deadline TIMESTAMP,
    created_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (artist_id) REFERENCES user(user_id)
);

CREATE TABLE IF NOT EXISTS "Insurance" (
    insurance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    commission_id INTEGER,
    is_insured INTEGER,
    coverage_details TEXT,
    price INTEGER,
    terms TEXT,
    created_at TIMESTAMP,
    FOREIGN KEY (commission_id) REFERENCES Commission(commission_id)
);

CREATE TABLE IF NOT EXISTS "Review" (
    review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    user_id INTEGER,
    rating INTEGER,
    comment TEXT,
    created_at TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES product(product_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE IF NOT EXISTS "Artist_Portfolio" (
    artist_portfolio_id INTEGER PRIMARY KEY AUTOINCREMENT,
    artist_id INTEGER,
    artwork_name TEXT,
    description TEXT,
    medium TEXT,
    image_url TEXT,
    created_at TIMESTAMP,
    FOREIGN KEY (artist_id) REFERENCES user(user_id)
);
''')

# Function to populate the database with sample data
def populate_database():
    # Populate categories
    categories = [
        ("Painting", "Various styles of painting."),
        ("Sculpture", "Three-dimensional artworks."),
        ("Digital Art", "Art created digitally."),
        ("Photography", "Art captured through a camera."),
        ("Crafts", "Handmade decorative items.")
    ]
    
    for category in categories:
        cursor.execute('''
            INSERT INTO category (name, description)
            VALUES (?, ?)
        ''', category)

    # Populate users
    for i in range(1, 201):
        username = f'user{i}'
        password_hash = f'hash{i}'  # In practice, use proper hashing
        email = f'user{i}@example.com'
        phone_number = f'123-456-789{i % 10}'
        user_type = random.choice(['buyer', 'artist'])
        is_verified = random.choice([0, 1])
        cursor.execute('''
            INSERT INTO user (username, password_hash, email, phone_number, user_type, is_verified)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, password_hash, email, phone_number, user_type, is_verified))

    # Populate products
    for i in range(1, 201):
        name = f'Product {i}'
        description = f'Description for product {i}'
        price = random.randint(10, 500)
        stock_quantity = random.randint(1, 100)
        category_id = random.randint(1, len(categories))
        artist_id = random.randint(1, 200)  # Assuming user IDs 1-200 are artists
        rating = random.uniform(1, 5)
        dimensions = f'{random.randint(1, 100)} x {random.randint(1, 100)} cm'
        medium = random.choice(['Oil', 'Acrylic', 'Digital', 'Sculpture'])
        image_url = f'http://example.com/images/product_{i}.jpg'
        cursor.execute('''
            INSERT INTO product (name, description, price, stock_quantity, category_id, artist_id, rating, dimensions, medium, image_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, description, price, stock_quantity, category_id, artist_id, rating, dimensions, medium, image_url))

    # Populate carts
    for i in range(1, 201):
        user_id = random.randint(101, 200)  # Assuming buyers have user_id 101-200
        created_at = random_date(datetime(2024, 1, 1), datetime(2024, 12, 31))
        updated_at = created_at + timedelta(hours=random.randint(1, 24))
        cursor.execute('''
            INSERT INTO Cart (user_id, created_at, updated_at)
            VALUES (?, ?, ?)
        ''', (user_id, created_at, updated_at))

    # Populate cart items
    for i in range(1, 201):
        cart_id = random.randint(1, 200)  # Assuming cart IDs are 1-200
        product_id = random.randint(1, 200)  # Assuming product IDs are 1-200
        quantity = random.randint(1, 5)
        price_per_unit = random.randint(10, 500)
        cursor.execute('''
            INSERT INTO Cart_Item (cart_id, product_id, quantity, price_per_unit)
            VALUES (?, ?, ?, ?)
        ''', (cart_id, product_id, quantity, price_per_unit))

    # Populate orders
    for i in range(1, 201):
        user_id = random.randint(101, 200)  # Assuming buyers have user_id 101-200
        order_date = random_date(datetime(2024, 1, 1), datetime(2024, 12, 31))
        total_amount = random.randint(10, 2000)
        order_status = random.choice(['Pending', 'Shipped', 'Delivered', 'Cancelled'])
        cursor.execute('''
            INSERT INTO "Order" (user_id, order_date, total_amount, order_status)
            VALUES (?, ?, ?, ?)
        ''', (user_id, order_date, total_amount, order_status))

    # Populate order items
    for i in range(1, 201):
        order_id = random.randint(1, 200)  # Assuming order IDs are 1-200
        product_id = random.randint(1, 200)  # Assuming product IDs are 1-200
        quantity = random.randint(1, 5)
        price_per_unit = random.randint(10, 500)
        cursor.execute('''
            INSERT INTO Order_Item (order_id, product_id, quantity, price_per_unit)
            VALUES (?, ?, ?, ?)
        ''', (order_id, product_id, quantity, price_per_unit))

    # Populate commissions
    for i in range(1, 201):
        user_id = random.randint(101, 200)  # Assuming buyers have user_id 101-200
        artist_id = random.randint(1, 200)  # Assuming user IDs 1-200 are artists
        description = f'Commission for user {user_id}'
        agreed_price = random.randint(50, 1000)
        status = random.choice(['Pending', 'In Progress', 'Completed', 'Cancelled'])
        deadline = random_date(datetime(2024, 1, 1), datetime(2024, 12, 31))
        created_at = random_date(datetime(2024, 1, 1), datetime(2024, 12, 31))
        cursor.execute('''
            INSERT INTO Commission (user_id, artist_id, description, agreed_price, status, deadline, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, artist_id, description, agreed_price, status, deadline, created_at))

    # Populate insurance
    for i in range(1, 201):
        commission_id = random.randint(1, 200)  # Assuming commission IDs are 1-200
        is_insured = random.choice([0, 1])
        coverage_details = f'Coverage for commission {commission_id}'
        price = random.randint(10, 100)
        terms = f'Terms for insurance {commission_id}'
        created_at = random_date(datetime(2024, 1, 1), datetime(2024, 12, 31))
        cursor.execute('''
            INSERT INTO Insurance (commission_id, is_insured, coverage_details, price, terms, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (commission_id, is_insured, coverage_details, price, terms, created_at))

    # Populate reviews
    for i in range(1, 201):
        product_id = random.randint(1, 200)  # Assuming product IDs are 1-200
        user_id = random.randint(101, 200)  # Assuming buyers have user_id 101-200
        rating = random.randint(1, 5)
        comment = f'Review comment for product {product_id}'
        created_at = random_date(datetime(2024, 1, 1), datetime(2024, 12, 31))
        cursor.execute('''
            INSERT INTO Review (product_id, user_id, rating, comment, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (product_id, user_id, rating, comment, created_at))

    # Populate artist portfolios
    for i in range(1, 201):
        artist_id = random.randint(1, 200)  # Assuming user IDs 1-200 are artists
        artwork_name = f'Artwork {i}'
        description = f'Description for artwork {i}'
        medium = random.choice(['Oil', 'Acrylic', 'Digital', 'Sculpture'])
        image_url = f'http://example.com/images/artwork_{i}.jpg'
        created_at = random_date(datetime(2024, 1, 1), datetime(2024, 12, 31))
        cursor.execute('''
            INSERT INTO Artist_Portfolio (artist_id, artwork_name, description, medium, image_url, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (artist_id, artwork_name, description, medium, image_url, created_at))

    # Commit changes
    conn.commit()

# Run the population function
populate_database()

# Close the connection
conn.close()
