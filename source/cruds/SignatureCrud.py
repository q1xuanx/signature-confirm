from asyncpg import Connection, Record
from ..schemas.SignatureSchema import SaveSignature, UpdatedSignature
from typing import List

async def create_signature(conn : Connection, signature : SaveSignature) -> bool: 
    result = await conn.execute('INSERT INTO signature(full_name, image_signature) VALUES($1, $2)', signature.full_name, signature.image_signature)
    if result.startswith('INSERT'):
        return True
    return False

async def get_list_signature(conn : Connection) -> List[Record]: 
    result = await conn.fetch('SELECT * FROM signature')
    return result

async def update_signature(conn : Connection, updated : UpdatedSignature): 
    result = await conn.execute('UPDATE signature SET image_signature = $1 WHERE stt = $2', updated.image_signature, updated.stt)
    if result.startswith('UPDATE'):
        return True
    return False
