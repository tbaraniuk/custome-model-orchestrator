CREATE TABLE IF NOT EXISTS performances (
    id SERIAL PRIMARY KEY,
    model_name TEXT NOT NULL,
    model_size TEXT NOT NULL,
    avg_infer_time FLOAT,
    times INT,
    img_width FLOAT,
    img_height FLOAT,
    datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
