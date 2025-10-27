# strawberry-spike

A tiny GraphQL spike using Strawberry and PostgreSQL.

## Quick start

Prerequisites:
- Docker
- Python 3.10+ and pip

From the project root:

1. Start PostgreSQL with seed data:
   ```bash
   docker compose up -d
   ```
2. (Optional) Create and activate a virtualenv:
   ```bash
   python3 -m venv virtualenv
   source virtualenv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the server:
   ```bash
   strawberry dev app.graphql.schema --host localhost
   ```
5. Open GraphiQL:
   ```
   http://localhost:8000/graphql
   ```

## Export GraphQL schema (SDL)

- Print SDL to stdout:
  ```bash
  strawberry export-schema app.graphql.schema
  ```
- Save SDL to a file:
  ```bash
  strawberry export-schema app.graphql.schema --output schema.graphql
  ```

## Example queries and use-cases

---

### 1) Query books
Simple list of books with their ids and titles.
```graphql
{
  books {
    id
    title
  }
}
```

### 2) Query books using startsWith
Filter books by a case-insensitive prefix on `title`.
```graphql
{
  books(startsWith: "har") {
    id
    title
  }
}
```
Tip: Try different prefixes (e.g., `"H"`, `"ha"`) — filtering uses a case-insensitive index for speed.

### 3) Query books and authors (unoptimized; demonstrates N+1)
This uses the `author` field, which resolves each book’s author with an individual SQL query. With SQL logging on, you’ll see a SELECT per book (N+1 pattern).
```graphql
{
  books {
    id
    title
    author {
      id
      name
    }
  }
}
```
What to observe in logs:
- Multiple statements like:
    - `SELECT a.id, a.name FROM public.authors a WHERE a.id = :id LIMIT 1`
- One per returned book that has an `author_id`.

### 4) Query books and authors_dataloader (optimized; batched)
This uses the `authorDataloader` field, which batches the author lookups for all books into a single query using `IN (...)`.
```graphql
{
  books {
    id
    title
    authorDataloader {
      id
      name
    }
  }
}
```
What to observe in logs:
- A single statement (per batch) like:
    - `SELECT a.id, a.name FROM public.authors a WHERE a.id IN (:ids_1, :ids_2, ...)`
- Confirms DataLoader batching avoided N+1.

### 5) Add book mutation
Creates a new book. The mutation uses an input type.
```graphql
mutation AddBookExample {
  addBook(input: { title: "New Title", authorId: "1" }) {
    id
    title
  }
}
```
Notes:
- `authorId` is optional. If omitted or invalid (non-numeric), the book is created without an author.
- If a non-existent numeric `authorId` is used and a foreign key constraint is active, the insert may fail and return `null`.

---
