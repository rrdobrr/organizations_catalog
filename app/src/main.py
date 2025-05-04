from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from .api.v1.routers import api_router
from .config.config import get_settings
from .middleware.api_secure import APIKeyMiddleware
from .core.exceptions_handler import setup_exception_handlers


settings = get_settings()


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API для мессенджера MyMessage",
    version=settings.VERSION,
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True,
    },
)


# Вспомогательная функция, добавляет в Swagger кнопку для авторизации по API_KEY
def add_api_key_field_to_swagger():
    HEADER_NAME = "x-api-key"
    if app.openapi_schema is not None:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    if "components" not in openapi_schema:
        openapi_schema["components"] = {}

    openapi_schema["components"]["securitySchemes"] = {
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": HEADER_NAME,
        }
    }

    openapi_schema["security"] = [{"ApiKeyAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

setup_exception_handlers(app)
app.add_middleware(APIKeyMiddleware)
app.openapi = add_api_key_field_to_swagger
app.include_router(api_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
