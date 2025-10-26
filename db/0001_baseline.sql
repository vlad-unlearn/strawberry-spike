-- Baseline schema for the application
-- This file resets migrations to a single baseline that can initialize a fresh DB.
-- It is safe to run multiple times on an existing database.

-- 1) Authors table
CREATE TABLE IF NOT EXISTS public.authors (
    id          BIGSERIAL PRIMARY KEY,
    name        TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Index to accelerate case-insensitive searches on author name
CREATE INDEX IF NOT EXISTS idx_authors_name_lower ON public.authors ((lower(name)));

-- 2) Books table (author_id present from the start)
CREATE TABLE IF NOT EXISTS public.books (
    id          BIGSERIAL PRIMARY KEY,
    title       TEXT NOT NULL,
    author_id   BIGINT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for books
CREATE INDEX IF NOT EXISTS idx_books_title_lower ON public.books ((lower(title)));
CREATE INDEX IF NOT EXISTS idx_books_author_id ON public.books (author_id);

-- Add FK from books.author_id to authors.id if missing
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM   pg_constraint c
        JOIN   pg_class t ON t.oid = c.conrelid
        WHERE  c.conname = 'fk_books_author'
        AND    t.relname = 'books'
    ) THEN
        ALTER TABLE public.books
            ADD CONSTRAINT fk_books_author
            FOREIGN KEY (author_id)
            REFERENCES public.authors(id)
            ON DELETE SET NULL
            ON UPDATE NO ACTION;
    END IF;
END $$;
