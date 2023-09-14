import json
import strawberry

from typing import Any

import pathlib


def load_data():
    data_path = pathlib.Path("data.json")

    if not data_path.exists():
        data_path.write_text("{}")

        return {}

    return json.loads(data_path.read_text())


def save_data(data: Any):
    data_path = pathlib.Path("data.json")
    data_path.touch(exist_ok=True)

    data_path.write_text(json.dumps(data))


@strawberry.type
class User:
    id: strawberry.ID
    name: str
    email: str
    books: list["Book"]


@strawberry.type
class Author:
    id: strawberry.ID
    name: str
    books: list["Book"]


@strawberry.type
class Book:
    id: strawberry.ID
    title: str
    published: int
    author: Author


@strawberry.type
class Query:
    @strawberry.field
    def all_users(self) -> list[User]:
        data = load_data()
        return [
            User(
                id=user["id"],
                name=user["name"],
                email=user["email"],
                books=[],
            )
            for user in data.get("users", [])
        ]

    @strawberry.field
    def user(self, id: strawberry.ID) -> User:
        data = load_data()
        return next((user for user in data.get("users", []) if user["id"] == id), None)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_user(self, name: str, email: str) -> User:
        data = load_data()
        data.setdefault("users", [])

        new_user = {
            "id": len(data["users"]) + 1,
            "name": name,
            "email": email,
            "books": [],
        }
        data["users"].append(new_user)
        save_data(data)
        return User(**new_user)


schema = strawberry.Schema(query=Query, mutation=Mutation)
