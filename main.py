from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from app.schema import schema

graphql_app = GraphQLRouter[None, None](schema, path="/")

app = FastAPI()
app.include_router(graphql_app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
