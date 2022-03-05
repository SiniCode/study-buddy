CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
);

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    sent_at TIMESTAMP,
    content TEXT,
    visible INTEGER
);

CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    question_id INTEGER REFERENCES questions ON DELETE SET NULL,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    sent_at TIMESTAMP,
    content TEXT,
    visible INTEGER
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
    user_id INTEGER REFERENCES users ON DELETE SET NULL,
    quiz_id INTEGER REFERENCES quizzes,
    score INTEGER
);
