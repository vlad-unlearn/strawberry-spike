from typing import Optional, List
from app.repositories.books import get_books as repo_get_books, add_book as repo_add_book
from app.graphql.types import Book


def get_books(starts_with: Optional[str]) -> List[Book]:
    rows = repo_get_books(starts_with)
    return [Book(id=r["id"], title=r["title"], author_id=r["author_id"]) for r in rows]


def add_book(title: str, author_id_raw: Optional[object]) -> Optional[Book]:
    """Create a new Book. author_id_raw may be a strawberry.ID or None."""
    # Convert incoming author ID to int if provided; ignore invalid values by treating as None
    author_id_int: Optional[int]
    if author_id_raw is None:
        author_id_int = None
    else:
        try:
            author_id_int = int(str(author_id_raw))
        except (ValueError, TypeError):
            author_id_int = None

    data = repo_add_book(title=title, author_id=author_id_int)
    if not data:
        return None
    return Book(id=data["id"], title=data["title"], author_id=data["author_id"])
