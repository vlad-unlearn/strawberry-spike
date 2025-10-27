import typing as t
import strawberry
from app.graphql.types import Book
from app.graphql.resolvers import get_books


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


schema = strawberry.Schema(query=Query)
