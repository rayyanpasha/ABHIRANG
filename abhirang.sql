-- Art Marketplace SQL Queries
-- ==========================

-- 1. User Management

-- a. Register a New User
INSERT INTO "user" (username, password_hash, email, phone_number, user_type, is_verified)
VALUES (?, ?, ?, ?, ?, 0);

-- b. Login User
SELECT username, user_type, is_verified 
FROM "user"
WHERE username = ? AND password_hash = ?;

-- c. Update User Verification (Admin Only)
UPDATE "user"
SET is_verified = 1
WHERE username = ?;


-- 2. Category Management

-- a. List All Categories
SELECT name, description 
FROM "category";

-- b. Add a New Category (Admin Only)
INSERT INTO "category" (name, description)
VALUES (?, ?);


-- 3. Product Management

-- a. Add a New Product (Artist Only)
INSERT INTO "product" (name, description, price, stock_quantity, category_id, artist_id, rating, dimensions, medium, image_url)
VALUES (?, ?, ?, ?, ?, ?, NULL, ?, ?, ?);

-- b. List Products by Category
SELECT name, description, price, stock_quantity 
FROM "product"
WHERE category_id = ?;

-- c. Display Product Details
SELECT p.name, p.description, p.price, p.stock_quantity, p.rating, c.name AS category_name, u.username AS artist_name
FROM "product" p
JOIN "category" c ON p.category_id = c.category_id
JOIN "user" u ON p.artist_id = u.user_id
WHERE p.name = ?;


-- 4. Cart and Order Management

-- a. Display Items in User’s Cart
SELECT ci.cart_id, p.name, ci.quantity, ci.price_per_unit, (ci.quantity * ci.price_per_unit) AS total_price
FROM "Cart_Item" ci
JOIN "Cart" c ON ci.cart_id = c.cart_id
JOIN "product" p ON ci.product_id = p.product_id
WHERE c.user_id = ?;

-- b. Add Item to Cart
INSERT INTO "Cart_Item" (cart_id, product_id, quantity, price_per_unit)
VALUES (?, ?, ?, ?);

-- c. Place an Order
INSERT INTO "Order" (user_id, order_date, total_amount, order_status)
VALUES (?, CURRENT_TIMESTAMP, ?, 'pending');

-- d. Add Order Items
INSERT INTO "Order_Item" (order_id, product_id, quantity, price_per_unit)
VALUES (?, ?, ?, ?);


-- 5. Commission Management

-- a. Request a Commission
INSERT INTO "Commission" (user_id, artist_id, description, agreed_price, status, deadline, created_at)
VALUES (?, ?, ?, ?, 'pending', ?, CURRENT_TIMESTAMP);

-- b. Update Commission Status (Artist Only)
UPDATE "Commission"
SET status = ?
WHERE commission_id = ? AND artist_id = ?;


-- 6. Insurance Management

-- a. Add Insurance for a Commission
INSERT INTO "Insurance" (commission_id, is_insured, coverage_details, price, terms, created_at)
VALUES (?, 1, ?, ?, ?, CURRENT_TIMESTAMP);


-- 7. Review Management

-- a. Add a Review for a Product
INSERT INTO "Review" (product_id, user_id, rating, comment, created_at)
VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP);

-- b. Display Reviews for a Product
SELECT r.rating, r.comment, r.created_at, u.username
FROM "Review" r
JOIN "user" u ON r.user_id = u.user_id
WHERE r.product_id = ?
ORDER BY r.created_at DESC;


-- 8. Artist Portfolio Management

-- a. Add Artwork to Portfolio (Artist Only)
INSERT INTO "Artist_Portfolio" (artist_id, artwork_name, description, medium, image_url, created_at)
VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP);

-- b. Display Portfolio of an Artist
SELECT artwork_name, description, medium, image_url
FROM "Artist_Portfolio"
WHERE artist_id = ?;


-- 9. Admin Dashboard Queries

-- a. Display Total Users and New Registrations
SELECT COUNT(username) AS total_users,
       COUNT(CASE WHEN created_at >= DATE('now', '-1 month') THEN 1 END) AS new_users_last_month
FROM "user";

-- b. Display Most Sold Products
SELECT p.name, COUNT(oi.order_id) AS total_sold, SUM(oi.price_per_unit * oi.quantity) AS total_revenue
FROM "product" p
JOIN "Order_Item" oi ON p.product_id = oi.product_id
GROUP BY p.name
ORDER BY total_sold DESC
LIMIT 10;


-- 10. Top-Selling Artist (Homepage)
SELECT u.username AS artist_name, COUNT(o.order_id) AS total_orders
FROM "user" u
JOIN "product" p ON u.user_id = p.artist_id
JOIN "Order_Item" oi ON p.product_id = oi.product_id
JOIN "Order" o ON oi.order_id = o.order_id
GROUP BY u.username
ORDER BY total_orders DESC
LIMIT 1;