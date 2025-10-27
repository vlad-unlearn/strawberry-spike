from typing import Optional, List, Dict, Any
from sqlalchemy import text, bindparam
from app.db import engine


def get_author_by_id(author_id: int) -> Optional[Dict[str, Any]]:
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT a.id, a.name FROM public.authors a WHERE a.id = :id LIMIT 1"),
                {"id": author_id},
            )
            row = result.mappings().first()
            return dict(row) if row else None
    except Exception:
        return None


def get_authors_by_ids(ids: List[int]) -> List[Dict[str, Any]]:
    if not ids:
        return []
    try:
        with engine.connect() as conn:
            stmt = (
                text("SELECT a.id, a.name FROM public.authors a WHERE a.id IN :ids")
                .bindparams(bindparam("ids", expanding=True))
            )
            result = conn.execute(stmt, {"ids": ids})
            return [dict(row) for row in result.mappings().all()]
    except Exception:
        return []
