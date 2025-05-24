from fastapi import FastAPI
from .routers import SignatureRouter
from contextlib import asynccontextmanager
from .utils.create_database import create_pool, close_pool

@asynccontextmanager
async def lifespan(app : FastAPI):
    app.state.db_pool = await create_pool()
    print('Create success')
    yield
    await close_pool(app.state.db_pool)

app = FastAPI(lifespan=lifespan)


app.include_router(router=SignatureRouter.router)


