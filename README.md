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
   strawberry dev schema
   ```
5. Open GraphiQL:
   ```
   http://localhost:8000/graphql
   ```

## Logging SQL queries (stdout)

Set SQLALCHEMY_ECHO to a truthy value to print executed SQL statements.

- Bash/Zsh:
  ```bash
  export SQLALCHEMY_ECHO=true && strawberry server schema
  ```
- PowerShell:
  ```powershell
  $Env:SQLALCHEMY_ECHO = "true"; strawberry server schema
  ```
- cmd.exe:
  ```bat
  set SQLALCHEMY_ECHO=true && strawberry server schema
  ```

## Export GraphQL schema (SDL)

- Print SDL to stdout:
  ```bash
  strawberry export-schema schema
  ```
- Save SDL to a file:
  ```bash
  strawberry export-schema schema --output schema.graphql
  ```
