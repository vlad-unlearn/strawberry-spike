import typing
import os

import strawberry
from sqlalchemy import create_engine, text

# Build a global SQLAlchemy engine (sync) using env vars (matches docker-compose defaults)
DB_USER = os.getenv("POSTGRES_USER", "app")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "app_password")
DB_NAME = os.getenv("POSTGRES_DB", "app_db")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = int(os.getenv("POSTGRES_PORT", "15432"))

DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, future=True, echo=True)


def get_books(
    starts_with: typing.Optional[str],
):
    base_sql = "SELECT b.title, b.author_id FROM public.books b"

    params: dict = {}
    where_clause = ""
    if starts_with is not None:
        # Use lower(...) LIKE lower(:starts_with) || '%' to leverage idx_books_title_lower
        where_clause = " WHERE lower(b.title) LIKE lower(:starts_with) || '%'"
        params = {"starts_with": starts_with}

    query = base_sql + where_clause + " ORDER BY b.title"

    try:
        with engine.connect() as conn:
            result = conn.execute(text(query), params)
            rows = result.mappings().all()
            return [
                Book(
                    title=row["title"],
                    author_id=row["author_id"],
                )
                for row in rows
            ]
    except Exception:
        return []
    

def get_author(author_id: strawberry.ID) -> typing.Optional["Author"]:
    try:
        # Validate/convert the incoming ID to an integer (authors.id is BIGINT)
        try:
            id_int = int(str(author_id))
        except (ValueError, TypeError):
            return None
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT a.id, a.name FROM public.authors a WHERE a.id = :id LIMIT 1"),
                {"id": id_int},
            )
            row = result.mappings().first()
            if not row:
                return None
            return Author(id=row["id"], name=row["name"])    
    except Exception:
        return None


@strawberry.type
class Book:
    title: str
    author_id: strawberry.Private[strawberry.ID]
    author: typing.Optional["Author"] = strawberry.field(resolver=lambda root: get_author(root.author_id))


@strawberry.type
class Author:
    id: strawberry.ID
    name: str


@strawberry.type
class Query:
    @strawberry.field
    def books(
        self,
        starts_with: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(
                name="startsWith",
                description="Type beginning of the book title",
            ),
        ] = None,
    ) -> typing.List[Book]:
        return get_books(starts_with=starts_with)

    @strawberry.field
    def author(
        self,
        author_id: typing.Annotated[
            strawberry.ID,
            strawberry.argument(name="authorId", description="Author ID"),
        ],
    ) -> typing.Optional[Author]:
        return get_author(author_id)


schema = strawberry.Schema(query=Query)
