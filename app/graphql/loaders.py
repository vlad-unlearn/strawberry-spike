from typing import Optional, List, Dict
import asyncio
from strawberry.dataloader import DataLoader
from app.repositories.authors import get_authors_by_ids


async def _batch_load_authors(keys: List[object]) -> List[Optional["Author"]]:
    # Normalize keys to ints; keep position and handle invalids
    normalized: List[Optional[int]] = []
    valid: List[int] = []
    for k in keys:
        try:
            n = int(str(k))
        except (TypeError, ValueError):
            n = None
        normalized.append(n)
        if n is not None:
            valid.append(n)

    if not valid:
        return [None for _ in keys]

    rows = await asyncio.to_thread(get_authors_by_ids, valid)
    by_id: Dict[int, tuple[str, str]] = {int(r["id"]): (str(r["id"]), r["name"]) for r in rows}

    from app.graphql.types import Author  # local import to avoid cycles

    out: List[Optional[Author]] = []
    for n in normalized:
        if n is None or n not in by_id:
            out.append(None)
        else:
            aid, name = by_id[n]
            out.append(Author(id=aid, name=name))
    return out


def get_or_create_author_loader(context: dict) -> DataLoader:
    key = "author_loader"
    loader = context.get(key)
    if loader is None:
        loader = DataLoader(load_fn=_batch_load_authors)
        context[key] = loader
    return loader
