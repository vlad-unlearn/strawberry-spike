import typing as t
import strawberry
from app.graphql.types import Book
from app.graphql.resolvers import get_books, add_book as add_book_resolver


@strawberry.type
class Query:
    @strawberry.field
    def books(
        self,
        starts_with: t.Annotated[
            t.Optional[str],
            strawberry.argument(
                name="startsWith",
                description="Type beginning of the book title",
            ),
        ] = None,
    ) -> list[Book]:
        return get_books(starts_with)


@strawberry.type
class Mutation:
    @strawberry.mutation(name="addBook")
    def add_book(
        self,
        title: str,
        author_id: t.Annotated[
            t.Optional[strawberry.ID],
            strawberry.argument(name="authorId", description="Adds a Book"),
        ] = None,
    ) -> t.Optional[Book]:
        return add_book_resolver(title, author_id)


schema = strawberry.Schema(query=Query, mutation=Mutation)
