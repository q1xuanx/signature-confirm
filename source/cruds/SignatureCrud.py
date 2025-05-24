from asyncpg import Connection, Record
from ..schemas.SignatureSchema import SaveSignature
from typing import List

async def create_signature(conn : Connection, signature : SaveSignature) -> bool: 
    result = await conn.execute('INSERT INTO signature(full_name, image_signature) VALUES($1, $2)', signature.full_name, signature.image_signature)
    if result.startswith('INSERT'):
        return True
    return False


async def get_list_signature(conn : Connection) -> List[Record]: 
    result = await conn.fetch('SELECT * FROM signature')
    return result
