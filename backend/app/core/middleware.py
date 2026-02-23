import time
import uuid
from fastapi import Request
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        logger.info(f"Request {request_id} started: {request.method} {request.url.path}")
        start_time = time.time()

        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            logger.info(f"Request {request_id} completed in {process_time:.4f}s with status {response.status_code}")
            response.headers["X-Request-ID"] = request_id
            return response
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(f"Request {request_id} failed after {process_time:.4f}s: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error", "request_id": request_id}
            )

def setup_logging():
    logger.add("logs/app.log", rotation="500 MB", level="INFO")
