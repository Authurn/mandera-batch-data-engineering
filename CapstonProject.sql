SELECT 
    o.order_id,
    o.order_date,
    c.customername,
    c.city,
    c.state,
    p.category,
    p."sub-category",
    od.quantity,
    od.amount,
    od.profit
FROM order_details od
JOIN orders o ON od.order_uid = o.order_uid
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON od.product_id = p.product_id
ORDER BY o.order_date DESC;

SELECT 
    c.customername,
    c.city,
    c.state,
    SUM(od.amount) AS total_spent,
    SUM(od.profit) AS total_profit
FROM order_details od
JOIN orders o ON od.order_uid = o.order_uid
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customername, c.city, c.state
ORDER BY total_spent DESC;

SELECT 
    p.category,
    SUM(od.amount) AS total_sales,
    SUM(od.profit) AS total_profit
FROM order_details od
JOIN products p ON od.product_id = p.product_id
GROUP BY p.category
ORDER BY total_sales DESC;

SELECT 
    p."sub-category" AS product,
    p.category,
    SUM(od.quantity) AS total_quantity_sold,
    SUM(od.amount) AS total_revenue
FROM order_details od
JOIN products p ON od.product_id = p.product_id
GROUP BY p."sub-category", p.category
ORDER BY total_revenue DESC
LIMIT 5;


SELECT 
    c.customername,
    SUM(od.profit) AS total_profit
FROM order_details od
JOIN orders o ON od.order_uid = o.order_uid
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customername
ORDER BY total_profit DESC
LIMIT 5;


SELECT 
    p.category,
    SUM(od.amount) AS total_sales,
    SUM(od.profit) AS total_profit,
    (SUM(od.profit) / SUM(od.amount) * 100) AS profit_margin_percent
FROM order_details od
JOIN products p ON od.product_id = p.product_id
GROUP BY p.category
ORDER BY profit_margin_percent DESC;

SELECT 
    c.customername,
    COUNT(o.order_uid) AS total_orders
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customername
HAVING COUNT(o.order_uid) > 1
ORDER BY total_orders DESC;

SELECT 
    p."sub-category" AS product,
    p.category,
    COUNT(od.product_id) AS times_ordered
FROM order_details od
JOIN products p ON od.product_id = p.product_id
GROUP BY p."sub-category", p.category
ORDER BY times_ordered DESC
LIMIT 1;


SELECT 
    o.paymentmode,
    COUNT(o.order_uid) AS total_orders,
    SUM(od.amount) AS total_revenue
FROM orders o
JOIN order_details od ON o.order_uid = od.order_uid
GROUP BY o.paymentmode
ORDER BY total_revenue DESC;

SELECT 
    o.order_date,
    SUM(od.amount) AS daily_sales,
    SUM(od.profit) AS daily_profit
FROM orders o
JOIN order_details od ON o.order_uid = od.order_uid
GROUP BY o.order_date
ORDER BY o.order_date ASC;

SELECT 
    o.order_date,
    SUM(od.amount) AS daily_sales,
    SUM(od.profit) AS daily_profit
FROM orders o
JOIN order_details od ON o.order_uid = od.order_uid
GROUP BY o.order_date
ORDER BY o.order_date ASC;

SELECT 
    c.customername,
    SUM(od.amount) AS total_spent,
    SUM(od.profit) AS total_profit
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_details od ON o.order_uid = od.order_uid
GROUP BY c.customername
ORDER BY total_spent DESC
LIMIT 5;

SELECT 
    c.state,
    c.city,
    SUM(od.amount) AS total_sales,
    SUM(od.profit) AS total_profit
FROM order_details od
JOIN orders o ON od.order_uid = o.order_uid
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.state, c.city
ORDER BY total_sales DESC;

SELECT 
    c.customername,
    COUNT(o.order_uid) AS total_orders
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customername
ORDER BY total_orders DESC
LIMIT 1;

SELECT * FROM customers;

SELECT customername, city, state FROM customers;

SELECT * FROM products LIMIT 5;

SELECT * FROM customers
ORDER BY customername ASC;  -- A to Z

SELECT DISTINCT state FROM customers;

SELECT * FROM orders
WHERE paymentmode = 'UPI';

SELECT * FROM order_details
WHERE quantity > 5;


SELECT * FROM customers
WHERE state = 'California' AND city = 'Los Angeles';


SELECT COUNT(*) FROM customers;

SELECT 
    o.order_id,
    c.customername,
    o.order_date
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id;


SELECT 
    order_id,
    SUM(amount) AS total_amount
FROM order_details
GROUP BY order_id;


SELECT product_id, category, "sub-category"
FROM products
LIMIT 10;


SELECT * FROM orders
ORDER BY order_date DESC;


SELECT * FROM customers
WHERE city = 'New York';
