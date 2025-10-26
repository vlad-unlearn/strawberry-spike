import typing
from pydoc import describe

import strawberry

def get_books(
    starts_with: typing.Optional[str],
):
    books = [
        Book(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
        ),
    ]
    if starts_with is not None:
        prefix = starts_with.lower()
        books = [b for b in books if b.title.lower().startswith(prefix)]
    return books

@strawberry.type
class Book:
    title: str
    author: str



@strawberry.type
class Query:
    @strawberry.field
    def books(
        self,
        starts_with: typing.Annotated[str, strawberry.argument(name="startsWith", description="Type beginning of the book title")],
    ) -> typing.List[Book]:
        return get_books(starts_with=starts_with)

schema = strawberry.Schema(query=Query)
