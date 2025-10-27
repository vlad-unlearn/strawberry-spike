import typing as t
import strawberry
from app.graphql.loaders import get_or_create_author_loader


@strawberry.type
class Author:
    id: strawberry.ID
    name: str


@strawberry.type
class Book:
    title: str
    author_id: strawberry.Private[strawberry.ID]

    @strawberry.field
    async def author(self: "Book", info: strawberry.types.Info) -> t.Optional[Author]:
        loader = get_or_create_author_loader(info.context)
        return await loader.load(self.author_id)
