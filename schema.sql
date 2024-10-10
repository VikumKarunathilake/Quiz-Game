-- Enable foreign key support
PRAGMA foreign_keys = ON;

-- Users table
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE COLLATE NOCASE,
    password TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create index on username for faster lookups
CREATE INDEX IF NOT EXISTS idx_user_username ON user(username);

-- Quizzes table
CREATE TABLE IF NOT EXISTS quiz (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

-- Create indexes for quiz lookups
CREATE INDEX IF NOT EXISTS idx_quiz_user_id ON quiz(user_id);
CREATE INDEX IF NOT EXISTS idx_quiz_created_at ON quiz(created_at DESC);

-- Questions table
CREATE TABLE IF NOT EXISTS question (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_text TEXT NOT NULL,
    quiz_id INTEGER NOT NULL,
    FOREIGN KEY (quiz_id) REFERENCES quiz(id) ON DELETE CASCADE
);

-- Create index for faster question lookups
CREATE INDEX IF NOT EXISTS idx_question_quiz_id ON question(quiz_id);

-- Answers table
CREATE TABLE IF NOT EXISTS answer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    answer_text TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL DEFAULT 0,
    question_id INTEGER NOT NULL,
    FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE
);

-- Create indexes for answer lookups
CREATE INDEX IF NOT EXISTS idx_answer_question_id ON answer(question_id);
CREATE INDEX IF NOT EXISTS idx_answer_is_correct ON answer(is_correct);

-- Results table
CREATE TABLE IF NOT EXISTS result (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    score INTEGER NOT NULL,
    taken_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    quiz_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (quiz_id) REFERENCES quiz(id) ON DELETE CASCADE
);

-- Create indexes for result lookups
CREATE INDEX IF NOT EXISTS idx_result_user_id ON result(user_id);
CREATE INDEX IF NOT EXISTS idx_result_quiz_id ON result(quiz_id);
CREATE INDEX IF NOT EXISTS idx_result_taken_at ON result(taken_at DESC);

-- Views for common queries

-- View for quiz statistics
CREATE VIEW IF NOT EXISTS quiz_stats AS
SELECT 
    q.id AS quiz_id,
    q.title AS quiz_title,
    u.username AS creator,
    COUNT(DISTINCT que.id) AS question_count,
    COUNT(DISTINCT r.id) AS times_taken,
    COALESCE(AVG(CAST(r.score AS FLOAT)), 0) AS average_score
FROM quiz q
JOIN user u ON q.user_id = u.id
LEFT JOIN question que ON q.id = que.quiz_id
LEFT JOIN result r ON q.id = r.quiz_id
GROUP BY q.id;

-- View for user statistics
CREATE VIEW IF NOT EXISTS user_stats AS
SELECT 
    u.id AS user_id,
    u.username,
    COUNT(DISTINCT q.id) AS quizzes_created,
    COUNT(DISTINCT r.id) AS quizzes_taken,
    COALESCE(AVG(CAST(r.score AS FLOAT)), 0) AS average_score
FROM user u
LEFT JOIN quiz q ON u.id = q.user_id
LEFT JOIN result r ON u.id = r.user_id
GROUP BY u.id;

-- Triggers for data integrity

-- Ensure at least one answer per question is correct
CREATE TRIGGER IF NOT EXISTS ensure_correct_answer
AFTER INSERT ON question
BEGIN
    INSERT INTO answer (answer_text, is_correct, question_id)
    VALUES ('Default correct answer', 1, NEW.id);
END;

-- Ensure quiz titles are not empty
CREATE TRIGGER IF NOT EXISTS ensure_quiz_title
BEFORE INSERT ON quiz
BEGIN
    SELECT
        CASE 
            WHEN NEW.title IS NULL OR trim(NEW.title) = ''
            THEN RAISE(ABORT, 'Quiz title cannot be empty')
        END;
END;

-- Example data insertion
INSERT OR IGNORE INTO user (username, password)
VALUES ('admin', 'hashed_password_here');

INSERT OR IGNORE INTO quiz (title, description, user_id)
SELECT 'Sample Quiz', 'This is a sample quiz', id
FROM user
WHERE username = 'admin'
LIMIT 1;

INSERT OR IGNORE INTO question (question_text, quiz_id)
SELECT 'What is the capital of France?', id
FROM quiz
LIMIT 1;

INSERT OR IGNORE INTO answer (answer_text, is_correct, question_id)
SELECT 'Paris', 1, id
FROM question
LIMIT 1;