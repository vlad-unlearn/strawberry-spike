strawberry-spike

A tiny GraphQL spike using Strawberry and PostgreSQL.

Quick start

- Prerequisites: Docker, Python 3.10+ and pip.
- In a terminal at the project root:
  1) Start PostgreSQL with seed data: docker compose up -d
  2) (Optional) Create a virtualenv: python -m venv .venv && source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
  3) Install deps: pip install -r requirements.txt
  4) Run the server: strawberry server schema
  5) Open http://127.0.0.1:8000/graphql

Logging SQL queries (stdout)

- Set SQLALCHEMY_ECHO to a truthy value to print executed SQL statements.
  - Bash/Zsh: export SQLALCHEMY_ECHO=true && strawberry server schema
  - PowerShell: $Env:SQLALCHEMY_ECHO = "true"; strawberry server schema
  - cmd.exe: set SQLALCHEMY_ECHO=true && strawberry server schema
