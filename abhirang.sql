-- SQL script for AbhiRang art marketplace

-- 1. User Registration
-- Adding a new user to the user table
INSERT INTO user (username, password_hash, email, phone_number, user_type, is_verified)
VALUES ('new_user', 'hashed_password', 'new_user@example.com', '123-456-7890', 'buyer', 0);

-- 2. User Login
-- Verifying user credentials
SELECT * FROM user 
WHERE username = 'existing_user' 
AND password_hash = 'hashed_password';

-- 3. View User Profile
-- Fetching details of a logged-in user
SELECT * FROM user 
WHERE username = 'logged_in_user';

-- 4. Update User Profile
-- Updating the user's email and phone number
UPDATE user 
SET email = 'new_email@example.com', 
    phone_number = '987-654-3210', 
    is_verified = 1 
WHERE username = 'logged_in_user';

-- 5. Add Product to Cart
-- Adding a new cart for the user
INSERT INTO Cart (user_id, created_at, updated_at)
VALUES (1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Adding a product to the cart
INSERT INTO Cart_Item (cart_id, product_id, quantity, price_per_unit)
VALUES ((SELECT cart_id FROM Cart WHERE user_id = 1 ORDER BY created_at DESC LIMIT 1), 
        2, 1, (SELECT price FROM product WHERE product_id = 2));

-- 6. View Cart Items
-- Displaying all items in the user's cart
SELECT ci.cart_item_id, p.name, ci.quantity, ci.price_per_unit
FROM Cart_Item ci
JOIN Cart c ON ci.cart_id = c.cart_id
JOIN product p ON ci.product_id = p.product_id
WHERE c.user_id = 1;  -- Replace with logged-in user's ID

-- 7. Remove Item from Cart
-- Deleting an item from the cart
DELETE FROM Cart_Item 
WHERE cart_item_id = 1;  -- Replace with the ID of the item to be removed

-- 8. Checkout
-- Creating an order for the user
INSERT INTO "Order" (user_id, order_date, total_amount, order_status)
VALUES (1, CURRENT_TIMESTAMP, (SELECT SUM(quantity * price_per_unit) FROM Cart_Item WHERE cart_id = (SELECT cart_id FROM Cart WHERE user_id = 1)), 'Pending');

-- Adding order items to the Order_Item table
INSERT INTO Order_Item (order_id, product_id, quantity, price_per_unit)
SELECT (SELECT order_id FROM "Order" ORDER BY order_date DESC LIMIT 1), 
       product_id, quantity, price_per_unit
FROM Cart_Item
WHERE cart_id = (SELECT cart_id FROM Cart WHERE user_id = 1);

-- 9. Leave a Review
-- Submitting a review for a product
INSERT INTO Review (product_id, user_id, rating, comment, created_at)
VALUES (2, 1, 5, 'This is an amazing product!', CURRENT_TIMESTAMP);

-- 10. View Reviews for a Product
-- Fetching all reviews for a specific product
SELECT r.rating, r.comment, u.username, r.created_at
FROM Review r
JOIN user u ON r.user_id = u.user_id
WHERE r.product_id = 2;  -- Replace with the product ID

-- 11. View Artist's Portfolio
-- Displaying all artworks from an artist's portfolio
SELECT ap.artwork_name, ap.description, ap.medium, ap.image_url
FROM Artist_Portfolio ap
WHERE ap.artist_id = 1;  -- Replace with the artist's ID

-- 12. Search Products
-- Searching for products by name or category
SELECT * FROM product 
WHERE name LIKE '%search_term%' 
   OR category_id IN (SELECT category_id FROM category WHERE name LIKE '%search_term%');

-- 13. View Categories
-- Displaying all available categories
SELECT * FROM category;

-- 14. Get User Orders
-- Fetching all orders made by a user
SELECT o.order_id, o.order_date, o.total_amount, o.order_status
FROM "Order" o
WHERE o.user_id = 1;  -- Replace with the logged-in user's ID

-- 15. Get Order Details
-- Viewing the details of a specific order
SELECT oi.product_id, p.name, oi.quantity, oi.price_per_unit
FROM Order_Item oi
JOIN product p ON oi.product_id = p.product_id
WHERE oi.order_id = 1;  -- Replace with the order ID
