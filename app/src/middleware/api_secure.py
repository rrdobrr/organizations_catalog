from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
import os

HEADER_NAME = "x-api-key"
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise RuntimeError("API_KEY не задан в переменных окружения")


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/docs") or request.url.path.startswith(
            "/openapi"
        ):
            return await call_next(request)

        api_key = request.headers.get(HEADER_NAME)
        if api_key != API_KEY:
            return JSONResponse(
                status_code=403, content={"detail": "Неверный API ключ"}
            )

        return await call_next(request)
