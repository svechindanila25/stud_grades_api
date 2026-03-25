CREATE TABLE IF NOT EXISTS grades (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    group_number VARCHAR(10) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    grade INTEGER NOT NULL CHECK (grade >= 2 AND grade <= 5)
);