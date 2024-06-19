from fastapi import FastAPI
from app.v1.routes import qr_route
from app.middleware.limiter_middleware import RateLimiterMiddleware


app = FastAPI()

app.include_router(qr_route.router)
app.add_middleware(RateLimiterMiddleware)


