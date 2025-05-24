import asyncpg
from .settings import setting

async def create_pool() -> asyncpg.Pool:
    return await asyncpg.create_pool(
        user=setting.USERNAME,
        password=setting.PASSWORD,
        database=setting.DATABASE_NAME,
        host=setting.SERVER,
        port=setting.PORT
    )


async def close_pool(pool):
    await pool.close()