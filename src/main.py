from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import redis.asyncio as redis
import sys

sys.path.append("..")
from src.routes import contacts, auth
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

app = FastAPI()
origins = [ 
    "http://localhost:8000"
    "http://localhost:6379"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contacts.router, prefix='/api')
app.include_router(auth.router, prefix='/api')


@app.on_event("startup")
async def startup():
    """
    Creates a limit on the number of requests.

    :return: An object that helps limit requests.
    :rtype: None
    """
    r = await redis.Redis(host='localhost', port=6379, db=0, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(r)

@app.get("/", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
def read_root():
    """
    Creates the main API page.

    :return: Display as a dictionary on the main page.
    :rtype: dict
    """
    return {"message": "Hello World"}