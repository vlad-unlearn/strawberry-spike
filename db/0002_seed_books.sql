-- Seed up to 10 books and their authors.
-- Idempotent: each INSERT is guarded with WHERE NOT EXISTS checks.
-- This script assumes the baseline (0001_baseline.sql) is already applied.

BEGIN;

-- Ensure authors exist
INSERT INTO public.authors (name)
SELECT v.name
FROM (VALUES
    ('F. Scott Fitzgerald'),
    ('George Orwell'),
    ('J.K. Rowling'),
    ('Jane Austen'),
    ('J.R.R. Tolkien')
) AS v(name)
WHERE NOT EXISTS (
    SELECT 1 FROM public.authors a WHERE lower(a.name) = lower(v.name)
);

-- Helper CTE to map author names to IDs
WITH author_ids AS (
    SELECT id, name FROM public.authors
)
-- Insert books if they don't exist yet (by title, case-insensitive)
INSERT INTO public.books (title, author_id)
SELECT b.title, a.id
FROM (
    VALUES
        ('The Great Gatsby', 'F. Scott Fitzgerald'),
        ('1984', 'George Orwell'),
        ('Animal Farm', 'George Orwell'),
        ('Harry Potter and the Sorcer\''s Stone', 'J.K. Rowling'),
        ('Harry Potter and the Chamber of Secrets', 'J.K. Rowling'),
        ('Pride and Prejudice', 'Jane Austen'),
        ('Sense and Sensibility', 'Jane Austen'),
        ('The Hobbit', 'J.R.R. Tolkien'),
        ('The Fellowship of the Ring', 'J.R.R. Tolkien'),
        ('The Two Towers', 'J.R.R. Tolkien')
) AS b(title, author_name)
JOIN author_ids a ON lower(a.name) = lower(b.author_name)
WHERE NOT EXISTS (
    SELECT 1 FROM public.books x WHERE lower(x.title) = lower(b.title)
);

COMMIT;
