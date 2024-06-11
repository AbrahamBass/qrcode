import uvicorn
from fastapi import FastAPI
from src.v1.routes import qr_route
from src.middleware.limiter_middleware import RateLimiterMiddleware

app = FastAPI()

app.include_router(qr_route.router)

app.add_middleware(RateLimiterMiddleware)

if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")


