SELECT
    category,
    COUNT(*) AS total_products,
    AVG(price) AS avg_price
FROM raw_products
GROUP BY category