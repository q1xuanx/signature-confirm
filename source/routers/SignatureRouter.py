from fastapi import APIRouter, Form
from typing import Annotated

from ..schemas.SignatureSchema import OwnerSignature

router = APIRouter(tags=['Signature Manage'])

@router.post(path='/create')
async def create_signature(data : Annotated[OwnerSignature, Form(media_type='multipart/form-data')]):
    return 'Hello ???'