from typing import Optional, List, Dict, Any
from sqlalchemy import text
from app.db import engine


def get_books(starts_with: Optional[str]) -> List[Dict[str, Any]]:
    base_sql = "SELECT b.title, b.author_id FROM public.books b"

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
