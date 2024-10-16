-- Verify the product table
SELECT * FROM "product" LIMIT 10;

-- Verify the category table
SELECT * FROM "category" LIMIT 10;

-- Verify the user table
SELECT * FROM "user" LIMIT 10;

-- Verify the Cart table
SELECT * FROM "Cart" LIMIT 10;

-- Verify the Cart_Item table
SELECT * FROM "Cart_Item" LIMIT 10;

-- Verify the Review table
SELECT * FROM "Review" LIMIT 10;

-- Verify the Commission table
SELECT * FROM "Commission" LIMIT 10;

-- Verify the Insurance table
SELECT * FROM "Insurance" LIMIT 10;

-- Verify the Order table
SELECT * FROM "Order" LIMIT 10;

-- Verify the Order_Item table
SELECT * FROM "Order_Item" LIMIT 10;

-- Verify the Artist_Portfolio table
SELECT * FROM "Artist_Portfolio" LIMIT 10;

-- Display the top-selling artists
SELECT u.username AS artist_name, COUNT(oi.product_id) AS total_sales
FROM "user" u
JOIN "product" p ON u.rowid = p.artist_id
JOIN "Order_Item" oi ON p.rowid = oi.product_id
GROUP BY u.username
ORDER BY total_sales DESC
LIMIT 5;

-- Display featured products based on rating
SELECT p.rowid AS product_id, p.name, p.price, p.rating
FROM "product" p
ORDER BY p.rating DESC, p.price DESC
LIMIT 10;

-- List all categories
SELECT rowid AS category_id, name, description
FROM "category"
ORDER BY name;

-- Display products in a selected category (use the category ID)
SELECT p.rowid AS product_id, p.name, p.price, p.stock_quantity
FROM "product" p
WHERE p.category_id = ?
ORDER BY p.name;

-- Display specific product details
SELECT p.rowid AS product_id, p.name, p.description, p.price, p.stock_quantity, p.rating, c.name AS category_name
FROM "product" p
JOIN "category" c ON p.category_id = c.rowid
WHERE p.rowid = ?;

-- Display reviews for a product
SELECT r.rowid AS review_id, r.rating, r.comment, r.created_at, u.username
FROM "Review" r
JOIN "user" u ON r.user_id = u.rowid
WHERE r.product_id = ?
ORDER BY r.created_at DESC;

-- Display items in a user’s cart
SELECT ci.rowid AS cart_item_id, p.name, ci.quantity, ci.price_per_unit, (ci.price_per_unit * ci.quantity) AS total_price
FROM "Cart_Item" ci
JOIN "Cart" c ON ci.cart_id = c.rowid
JOIN "product" p ON ci.product_id = p.rowid
WHERE c.user_id = ?;

-- Display order summary during checkout
SELECT oi.rowid AS order_item_id, p.name, oi.price_per_unit, oi.quantity, (oi.price_per_unit * oi.quantity) AS total_price
FROM "Order_Item" oi
JOIN "product" p ON oi.product_id = p.rowid
WHERE oi.order_id = ?;

-- Display recent orders
SELECT o.rowid AS order_id, o.order_date, o.total_amount, o.order_status
FROM "Order" o
WHERE o.user_id = ?
ORDER BY o.order_date DESC
LIMIT 10;

-- Display commissions placed by the user
SELECT c.rowid AS commission_id, c.description, c.agreed_price, c.status, c.created_at
FROM "Commission" c
WHERE c.user_id = ?
ORDER BY c.created_at DESC;

-- Display most sold products
SELECT p.rowid AS product_id, p.name, COUNT(oi.product_id) AS total_sold, SUM(oi.price_per_unit * oi.quantity) AS total_revenue
FROM "product" p
JOIN "Order_Item" oi ON p.rowid = oi.product_id
GROUP BY p.rowid, p.name
ORDER BY total_sold DESC
LIMIT 10;

-- Display total users and new registrations
SELECT COUNT(rowid) AS total_users, 
       COUNT(CASE WHEN u.created_at >= DATE('now', '-1 month') THEN 1 END) AS new_users_last_month
FROM "user" u;

-- Display most sold products
SELECT p.rowid AS product_id, p.name, COUNT(oi.product_id) AS total_sold, SUM(oi.price_per_unit * oi.quantity) AS total_revenue
FROM "product" p
JOIN "Order_Item" oi ON p.rowid = oi.product_id
GROUP BY p.rowid, p.name
ORDER BY total_sold DESC
LIMIT 10;

-- Display total users and new registrations
SELECT COUNT(rowid) AS total_users, 
       COUNT(CASE WHEN u.created_at >= DATE('now', '-1 month') THEN 1 END) AS new_users_last_month
FROM "user" u;

-- Display artist portfolio for a specific artist
SELECT ap.artwork_name, ap.description, ap.medium, ap.image_url, ap.created_at
FROM "Artist_Portfolio" ap
WHERE ap.artist_id = ?
ORDER BY ap.created_at DESC;
