SELECT
    product_name,
    COUNT(*) AS total_orders,
    SUM(quantity) AS total_quantity,
    SUM(amount) AS total_sales
FROM raw_orders
GROUP BY product_name