from pydantic import BaseModel
from fastapi import UploadFile

class OwnerSignature(BaseModel):
    full_name : str 
    image_signature : UploadFile


class SaveSignature(BaseModel):
    full_name : str 
    image_signature : str    