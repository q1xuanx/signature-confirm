from fastapi import APIRouter, Form, Depends
from typing import Annotated
from asyncpg import Connection
from ..utils.dependencies import get_db_connection
from ..schemas.SignatureSchema import OwnerSignature, UpdateSignature, VerifySignature
from ..services.SignatureService import createSignature, getListSignature, updateSignature, verifySignature

router = APIRouter(tags=['Signature Manage'])

@router.post(path='/create')
async def create(data : Annotated[OwnerSignature, Form(media_type='multipart/form-data')], conn : Connection = Depends(get_db_connection)):
    result = await createSignature(conn, data)
    if result:
        return { 
            'message': 'Add success'
        }
    return {
        'message': 'Add Fail'
    }

@router.get(path='/get-list')
async def get_lits(conn : Connection = Depends(get_db_connection)): 
    result = await getListSignature(conn)
    return {
        'data': result
    }

@router.post(path='/update')
async def update(update : Annotated[UpdateSignature, Form(media_type='multipart/form-data')], conn : Connection = Depends(get_db_connection)):
    result = await updateSignature(conn, update)
    if result:
        return {
            'message': 'Update Success'
        }
    return {
        'message': 'Update Fail'
    }

@router.post(path='/verify')
async def verify (verify : Annotated[VerifySignature, Form(media_type='multipart/form-data')], conn : Connection = Depends(get_db_connection)):
    result = await verifySignature(conn, verify)
    return result