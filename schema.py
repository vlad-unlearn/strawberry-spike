import typing
import os

import strawberry


def get_books(
    starts_with: typing.Optional[str],
):
    # Read DB connection settings (match docker-compose defaults)
    db_user = os.getenv("POSTGRES_USER", "app")
    db_password = os.getenv("POSTGRES_PASSWORD", "app_password")
    db_name = os.getenv("POSTGRES_DB", "app_db")
    db_host = os.getenv("POSTGRES_HOST", "localhost")
    db_port = int(os.getenv("POSTGRES_PORT", "15432"))

    sql = (
        """
        SELECT b.title, a.id AS author_id, a.name AS author_name
        FROM public.books b
        LEFT JOIN public.authors a ON a.id = b.author_id
        {where}
        ORDER BY b.title
        """
    )

    params: tuple = ()
    where_clause = ""
    if starts_with is not None:
        # Use lower(...) LIKE lower(%s) || '%' to leverage idx_books_title_lower
        where_clause = "WHERE lower(b.title) LIKE lower(%s) || '%'"
        params = (starts_with,)

    query = sql.format(where=where_clause)

    try:
        with psycopg.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                rows = cur.fetchall()
                return [
                    Book(
                        title=row[0],
                        author=(
                            Author(id=str(row[1]), name=row[2])
                            if row[1] is not None else None
                        ),
                    )
                    for row in rows
                ]
    except Exception:
        # In a real app, you'd log this.
        return []

@strawberry.type
class Book:
    title: str
    author: typing.Optional["Author"]



@strawberry.type
class Author:
    id: strawberry.ID
    name: str


@strawberry.type
class Query:
    @strawberry.field
    def books(
        self,
        starts_with: typing.Annotated[typing.Optional[str], strawberry.argument(name="startsWith", description="Type beginning of the book title")] = None,
    ) -> typing.List[Book]:
        return get_books(starts_with=starts_with)

schema = strawberry.Schema(query=Query)
