from typing import Optional, List
from app.repositories.books import get_books as repo_get_books
from app.graphql.types import Book


def get_books(starts_with: Optional[str]) -> List[Book]:
    rows = repo_get_books(starts_with)
    return [Book(title=r["title"], author_id=r["author_id"]) for r in rows]
