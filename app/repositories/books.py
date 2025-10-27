from typing import Optional, List, Dict, Any
from sqlalchemy import text
from app.db import engine


def get_books(starts_with: Optional[str]) -> List[Dict[str, Any]]:
    base_sql = "SELECT b.id, b.title, b.author_id FROM public.books b"

    params: dict = {}
    where_clause = ""
    if starts_with is not None:
        where_clause = " WHERE lower(b.title) LIKE lower(:starts_with) || '%'"
        params = {"starts_with": starts_with}

    query = base_sql + where_clause + " ORDER BY b.title"

    try:
        with engine.connect() as conn:
            result = conn.execute(text(query), params)
            return [dict(row) for row in result.mappings().all()]
    except Exception:
        return []


def add_book(title: str, author_id: Optional[int]) -> Optional[Dict[str, Any]]:
    """Insert a new book and return its title and author_id.
    Returns None on error.
    """
    try:
        with engine.begin() as conn:  # use transaction
            result = conn.execute(
                text(
                    """
                    INSERT INTO public.books (title, author_id)
                    VALUES (:title, :author_id) RETURNING id, title, author_id
                    """
                ),
                {"title": title, "author_id": author_id},
            )
            row = result.mappings().first()
            return dict(row) if row else None
    except Exception:
        return None
