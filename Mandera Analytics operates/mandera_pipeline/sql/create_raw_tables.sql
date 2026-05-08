CREATE TABLE IF NOT EXISTS raw_customers (
    id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT,
    country TEXT,
    status TEXT
);

CREATE TABLE IF NOT EXISTS raw_products (
    id SERIAL PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    price NUMERIC,
    stock INTEGER
);

CREATE TABLE IF NOT EXISTS raw_orders (
    id SERIAL PRIMARY KEY,
    customer_name TEXT,
    product_name TEXT,
    quantity INTEGER,
    amount NUMERIC,
    status TEXT
);