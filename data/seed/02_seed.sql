INSERT INTO customers (name, email, city) VALUES
('Alice Johnson', 'alice.johnson@example.com', 'New York'),
('Bob Smith', 'bob.smith@example.com', 'Los Angeles'),
('Carol Davis', 'carol.davis@example.com', 'Chicago'),
('David Wilson', 'david.wilson@example.com', 'Houston'),
('Emma Brown', 'emma.brown@example.com', 'Phoenix'),
('Frank Miller', 'frank.miller@example.com', 'Philadelphia'),
('Grace Lee', 'grace.lee@example.com', 'San Antonio'),
('Henry Clark', 'henry.clark@example.com', 'San Diego'),
('Ivy Turner', 'ivy.turner@example.com', 'Dallas'),
('Jack White', 'jack.white@example.com', 'San Jose'),
('Karen Hall', 'karen.hall@example.com', 'Austin'),
('Leo Young', 'leo.young@example.com', 'Jacksonville'),
('Mia King', 'mia.king@example.com', 'Columbus'),
('Noah Scott', 'noah.scott@example.com', 'Charlotte'),
('Olivia Adams', 'olivia.adams@example.com', 'Seattle');

INSERT INTO products (name, category, price) VALUES
('Wireless Mouse', 'Electronics', 25.99),
('Mechanical Keyboard', 'Electronics', 89.99),
('USB-C Hub', 'Electronics', 34.50),
('Office Chair', 'Furniture', 179.99),
('Standing Desk', 'Furniture', 349.00),
('Desk Lamp', 'Furniture', 42.75),
('Notebook Set', 'Stationery', 12.99),
('Fountain Pen', 'Stationery', 24.00),
('Backpack', 'Accessories', 59.99),
('Water Bottle', 'Accessories', 18.50),
('Noise Cancelling Headphones', 'Electronics', 199.99),
('Webcam HD', 'Electronics', 65.00);

-- customer_id, product_id, quantity, unit_price, status, order_date, refund_amount
INSERT INTO orders (customer_id, product_id, quantity, unit_price, status, order_date, refund_amount) VALUES
(1, 5, 2, 349.00, 'completed', '2026-06-05', 0),
(1, 11, 3, 199.99, 'completed', '2026-07-10', 0),
(1, 4, 2, 179.99, 'completed', '2026-08-02', 0),

(2, 5, 1, 349.00, 'completed', '2026-06-15', 0),
(2, 2, 4, 89.99, 'completed', '2026-07-01', 0),
(2, 11, 2, 199.99, 'completed', '2026-08-20', 0),
(2, 4, 1, 179.99, 'completed', '2026-09-01', 0),

(3, 5, 3, 349.00, 'completed', '2026-06-20', 0),
(3, 6, 5, 42.75, 'completed', '2026-07-15', 0),

(4, 11, 2, 199.99, 'completed', '2026-06-10', 0),
(4, 2, 2, 89.99, 'completed', '2026-08-05', 0),

(5, 9, 3, 59.99, 'completed', '2026-07-20', 0),
(5, 3, 4, 34.50, 'completed', '2026-08-10', 0),

(6, 1, 5, 25.99, 'completed', '2026-06-25', 0),
(6, 7, 10, 12.99, 'completed', '2026-08-01', 0),

(7, 8, 2, 24.00, 'completed', '2026-07-05', 0),
(7, 10, 3, 18.50, 'completed', '2026-08-12', 0),

(8, 12, 2, 65.00, 'completed', '2026-06-30', 0),

(9, 4, 1, 179.99, 'completed', '2026-07-25', 0),
(9, 11, 1, 199.99, 'refunded', '2026-08-15', 199.99),

(10, 2, 1, 89.99, 'refunded', '2026-08-18', 89.99),
(10, 1, 2, 25.99, 'completed', '2026-09-05', 0),

(11, 6, 2, 42.75, 'refunded', '2026-08-22', 85.50),

(12, 9, 1, 59.99, 'completed', '2026-09-10', 0),
(13, 3, 2, 34.50, 'completed', '2026-09-12', 0),
(14, 7, 5, 12.99, 'completed', '2026-09-15', 0),
(15, 10, 4, 18.50, 'completed', '2026-09-18', 0);
