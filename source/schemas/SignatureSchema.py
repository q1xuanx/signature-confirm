from pydantic import BaseModel
from fastapi import UploadFile

class OwnerSignature(BaseModel):
    full_name : str 
    image_signature : UploadFile

class UpdateSignature(BaseModel):
    stt : int
    image_signature : UploadFile

class SaveSignature(BaseModel):
    full_name : str 
    image_signature : str    

class UpdatedSignature(BaseModel):
    stt : int
    image_signature : str
    
class VerifySignature(BaseModel):
    image : UploadFile