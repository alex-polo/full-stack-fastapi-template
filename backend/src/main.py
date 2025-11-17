import contextlib

import uvicorn
from fastapi import FastAPI

from .api import api_router


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="", description="", lifespan=lifespan)

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8080, reload=True)
