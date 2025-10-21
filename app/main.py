import os
from fastapi import FastAPI
from dotenv import dotenv_values
from app.api.main import api_router
from app.core.config import settings
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


if settings.ENVIRONMENT == "local":
    os.environ.update(dotenv_values(".env"))


app = FastAPI(
    title=settings.PROJECT_NAME, generate_unique_id_function=custom_generate_unique_id
)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/", tags=["root"], response_model=dict)
def read_root() -> dict:
    return {
        "project": settings.PROJECT_NAME,
        "version": "1.0",
        "info": "Check the /docs routes",
    }


app.include_router(api_router)
