SELECT
    country,
    COUNT(*) AS total_customers
FROM raw_customers
GROUP BY country