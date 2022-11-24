from api.router import api_router
from fastapi import FastAPI


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="🏢 Inventory Managment",
        description="🏢 Inventory Managment Project",
        version="0.1",
        docs_url="/api/docs/",
        redoc_url="/api/redoc/",
        openapi_url="/api/openapi.json"
    )

    app.include_router(router=api_router)

    return app
