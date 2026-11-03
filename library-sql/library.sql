-- SQLite database with fictional sample records
PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS loans;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS students;
CREATE TABLE students (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE books (id INTEGER PRIMARY KEY, title TEXT NOT NULL, author TEXT NOT NULL);
CREATE TABLE loans (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id),
    book_id INTEGER NOT NULL REFERENCES books(id),
    borrowed_on TEXT NOT NULL,
    due_on TEXT NOT NULL,
    returned_on TEXT,
    CHECK (due_on >= borrowed_on)
);
INSERT INTO students VALUES (1, 'Alex'), (2, 'Taylor'), (3, 'Jordan');
INSERT INTO books VALUES (1, 'Introduction to Python', 'A. Writer'),
(2, 'Database Basics', 'B. Writer'), (3, 'Data Stories', 'C. Writer');
INSERT INTO loans VALUES
(1,1,1,'2026-09-01','2026-09-15','2026-09-12'),
(2,2,2,'2026-09-10','2026-09-24',NULL),
(3,3,1,'2026-10-01','2026-10-15',NULL),
(4,1,3,'2026-10-10','2026-10-24','2026-10-21'),
(5,2,1,'2026-10-20','2026-11-03',NULL);

-- Open loans overdue as of a fixed date (repeatable example)
SELECT s.name, b.title, l.due_on
FROM loans l JOIN students s ON s.id = l.student_id
JOIN books b ON b.id = l.book_id
WHERE l.returned_on IS NULL AND l.due_on < '2026-11-01'
ORDER BY l.due_on;

-- Most borrowed titles
SELECT b.title, COUNT(l.id) AS number_of_loans
FROM books b LEFT JOIN loans l ON l.book_id = b.id
GROUP BY b.id, b.title ORDER BY number_of_loans DESC;

-- Loan count for each student
SELECT s.name, COUNT(l.id) AS loans
FROM students s LEFT JOIN loans l ON l.student_id = s.id
GROUP BY s.id, s.name ORDER BY loans DESC;

-- Current unreturned count
SELECT COUNT(*) AS outstanding_loans FROM loans WHERE returned_on IS NULL;

-- Total borrowing by month
SELECT SUBSTR(borrowed_on,1,7) AS month, COUNT(*) AS loans
FROM loans GROUP BY SUBSTR(borrowed_on,1,7) ORDER BY month;
