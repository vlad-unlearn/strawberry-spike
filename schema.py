# Entry point shim for Strawberry
# Keeps the `strawberry server schema` command working
from app.graphql.schema import schema  # re-export
