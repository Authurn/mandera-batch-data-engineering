CREATE TABLE IF NOT EXISTS pipeline_monitoring (
    id SERIAL PRIMARY KEY,
    pipeline_name TEXT,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);