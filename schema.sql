CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    sender_id INTEGER REFERENCES users,
    sent_at TIMESTAMP,
    answer_to INTEGER REFERENCES messages,
    content TEXT,
    likes INTEGER
);
