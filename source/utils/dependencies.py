from fastapi import Request, HTTPException
from typing import AsyncGenerator
import asyncpg

async def get_db_connection(request : Request) -> AsyncGenerator[asyncpg.Connection, None]: 
    try: 
        pool = request.app.state.db_pool
        if pool is None:
            raise HTTPException(status_code=500, detail='Database pool not initialized')
        async with pool.acquire() as conn: 
            yield conn
    except Exception as e: 
        raise HTTPException(status_code=500, detail=f'Database connection error: {str(e)}')