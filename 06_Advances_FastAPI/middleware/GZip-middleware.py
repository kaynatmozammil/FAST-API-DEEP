from fastapi import FastAPI
from starlette.middleware.gzip import GZipMiddleware

app = FastAPI()

app.middleware(
    GZipMiddleware,
    minimun_size = 1000
)