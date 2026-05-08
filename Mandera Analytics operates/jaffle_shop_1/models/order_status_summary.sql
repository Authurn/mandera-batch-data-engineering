SELECT
    status,
    COUNT(*) AS total_orders,
    SUM(amount) AS total_sales
FROM raw_orders
GROUP BY status