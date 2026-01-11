from pydantic import BaseModel
from typing import List, Optional

class GetTokenStatusAPIResponseSchema(BaseModel):
    status: str

class CreateProtectedResourceAPIRequestSchema(BaseModel):
    name: str
    description: str

class CreateProtectedResourceAPIResponseSchema(BaseModel):
    resourceId: str
    name: str
    description: str

class GetProtectedResourceAPIResponseSchema(BaseModel):
    resourceId: str
    name: str
    description: str

class GetAllProtectedResourceAPIResponseSchema(BaseModel):
    items: List[GetProtectedResourceAPIResponseSchema]
    total: int

class UpdateProtectedResourceAPIRequestSchema(BaseModel):
    description: Optional[str] = None

class UpdateProtectedResourceAPIResponseSchema(BaseModel):
    resourceId: str
    name: str
    description: str

class DeleteProtectedResourceAPIResponseSchema(BaseModel):
    message: str