import typing as t
import strawberry
from app.graphql.loaders import get_or_create_author_loader

from app.repositories.authors import get_author_by_id as repo_get_author_by_id


@strawberry.type
class Author:
    id: strawberry.ID
    name: str


@strawberry.type
class Book:
    id: strawberry.ID
    title: str
    author_id: strawberry.Private[strawberry.ID]

    # Optimized resolver, uses Dataloader to avoid N+1 problem
    @strawberry.field
    async def author_dataloader(self: "Book", info: strawberry.types.Info) -> t.Optional[Author]:
        loader = get_or_create_author_loader(info.context)
        return await loader.load(self.author_id)

    # Unoptimized resolver runs a SQL query to get one author at a time, for each book
    @strawberry.field
    def author(self: "Book") -> t.Optional[Author]:
        # Convert strawberry.ID to int safely; return None for invalid/missing IDs
        try:
            aid = int(str(self.author_id)) if self.author_id is not None else None
        except (ValueError, TypeError):
            return None
        if aid is None:
            return None

        data = repo_get_author_by_id(aid)
        if not data:
            return None
        # Map repository dict to GraphQL Author type
        return Author(id=str(data["id"]), name=data["name"])
