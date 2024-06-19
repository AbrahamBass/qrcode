import time
from starlette.types import ASGIApp
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from collections import defaultdict
from typing import Dict


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.rate_limit_records: Dict[str, float] = defaultdict(float)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        client_ip = request.client.host
        current_time = time.time()

        if current_time - self.rate_limit_records[client_ip] < 1:
            return Response(content="Rate limit exceeded", status_code=429)

        self.rate_limit_records[client_ip] = current_time
        return await call_next(request)

