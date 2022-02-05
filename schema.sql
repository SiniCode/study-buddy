CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
);

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP,
    content TEXT
);

CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    answer_to INTEGER REFERENCES questions,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP,
    content TEXT,
    likes INTEGER
);

CREATE TABLE quizzes (
    id SERIAL PRIMARY KEY,
    name TEXT,
    description TEXT,
    visible INTEGER
);

CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER REFERENCES quizzes,
    task TEXT,
    solution TEXT
);

CREATE TABLE attempts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    quiz_id INTEGER REFERENCES quizzes,
    score INTEGER
);
